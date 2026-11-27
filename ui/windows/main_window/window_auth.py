import asyncio
from qasync import asyncSlot
from ui.common.PySide6_Qt import *

class WindowAuth:
    def reset_user_state(self):
        self.current_user = None
        self.current_profile = None

        self.page_manager = None
        self.sidebar = None
        self.toolbar = None

    def return_to_auth(self):
        self.reset_user_state()
        self.show_auth_ui()
        self.window_controls.raise_()

    async def handle_blocked_user(self):
        from services.supabase.supabase_auth import sign_out
        from services.supabase.supabase_session import clear_session

        if self.page_manager is not None:
            self.return_to_auth()

        self.auth_view.show_blocked()

        await self.stop_realtime()

        try:
            await sign_out()
        except Exception as error:
            print(f"Sign out failed: {error}")

        try:
            clear_session()
        except Exception as error:
            print(f"Session cleanup failed: {error}")
            return

        self.reset_user_state()
        self.auth_view.blocked_login.back_button.setEnabled(True)

    @asyncSlot(object)
    async def on_authenticated(self, user):
        if self.page_manager is not None:
            return

        self.current_user = user

        try:
            await self.load_user_profile()
        except Exception:
            self.reset_user_state()

            self.auth_view.switch_page(0)
            self.auth_view.set_loading(False)

            self.auth_view.alert.show_message(
                self.auth_view.messages["general"]["unexpected_error"]
            )
            return

        if self.current_profile["is_blocked"]:
            await self.handle_blocked_user()
            return

        self.show_main_ui()
        asyncio.create_task(self.start_realtime())

        if self.update_worker is None or not self.update_worker.isRunning():
            self.start_update_check()

    async def load_user_profile(self):
        from services.supabase.supabase_queries import get_user_profile
        from services.supabase.supabase_session import load_session
        from services.supabase.supabase_profile_cache import save_profile

        profile = await get_user_profile(self.current_user.id)
        self.current_profile = profile

        if profile["is_blocked"] or load_session() is None:
            return

        save_profile(
            self.current_user.id,
            profile.get("first_name", ""),
            profile.get("last_name", ""),
            self.current_user.email,
            profile.get("avatar")
        )

    @asyncSlot()
    async def handle_logout(self):
        from services.supabase.supabase_auth import sign_out

        if self.sidebar is None:
            return

        self.sidebar.profile.logout_button.setEnabled(False)

        try:
            await sign_out()
        except Exception:
            if self.sidebar is not None:
                self.sidebar.profile.logout_button.setEnabled(True)

                QMessageBox.warning(
                    self,
                    "Sign Out",
                    "Unable to sign out. Please try again."
                )
            return

        await self.stop_realtime()

        if self.page_manager is not None:
            self.return_to_auth()

    async def restore_user_session(self):
        from services.supabase.supabase_auth import restore_session
        from services.supabase.supabase_session import clear_session

        self.auth_view.set_loading(True)

        try:
            response = await restore_session()

            if response is not None and response.user is not None:
                await self.on_authenticated(response.user)

        except Exception as error:
            print(f"Session restore failed: {error}")
            clear_session()

        finally:
            if not self._closing and self.centralWidget() is self.auth_view:
                if self.auth_view.is_remembered_page:
                    self.auth_view.switch_page(0)

                self.auth_view.set_loading(False)