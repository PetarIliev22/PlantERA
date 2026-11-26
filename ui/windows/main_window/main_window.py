from qasync import asyncSlot
from ui.common.PySide6_Qt import *
from ui.components.window_controls import WindowControls
from ui.views.auth_views import AuthView
from .window_events import WindowEvents
from .window_appearance import WindowAppearance
from .window_updates import WindowUpdates

class MainWindow(WindowEvents, WindowAppearance, WindowUpdates, QMainWindow):
    def __init__(self):
        super().__init__()

        self._closing = False
        self.update_worker = None

        self.reset_user_state()

        self.setup_window()
        self.setup_timers()
        self.show_auth_ui()

        self.window_controls = WindowControls(self)
        self.window_controls.show()

        self.position_window_controls()

    def reset_user_state(self):
        self.current_user = None
        self.current_profile = None

        self.page_manager = None
        self.sidebar = None
        self.toolbar = None

    def show_auth_ui(self):
        self.auth_view = AuthView(self)
        self.setCentralWidget(self.auth_view)

        self.auth_view.login_handler.authenticated.connect(
            self.on_authenticated
        )

        self.auth_view.register_handler.authenticated.connect(
            self.on_authenticated
        )

    def show_main_ui(self):
        from ui.components.toolbar import Toolbar
        from ui.components.sidebar import Sidebar
        from core.page_manager import PageManager
        
        central = QWidget()
        central.setObjectName("mainContainer")
        self.setCentralWidget(central)
        self.window_controls.raise_()

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar(self)

        self.sidebar.profile.logout_requested.connect(
            self.handle_logout
        )

        self.sidebar.profile.set_profile(
            self.current_profile,
            self.current_profile.get("avatar")
        )

        main_layout.addWidget(self.sidebar)

        right_container = QWidget()
        right_container.setObjectName("mainContent")

        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.toolbar = Toolbar(self)
        right_layout.addWidget(self.toolbar)

        self.page_manager = PageManager(right_container)
        right_layout.addWidget(self.page_manager, 1)

        self.sidebar.page_changed.connect(
            self.page_manager.change_page
        )

        main_layout.addWidget(right_container, 1)

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

        self.show_main_ui()

        if self.update_worker is None or not self.update_worker.isRunning():
            self.start_update_check()

    async def load_user_profile(self):
        from services.supabase.supabase_queries import get_user_profile

        self.current_profile = await get_user_profile(
            self.current_user.id
        )

    @asyncSlot()
    async def handle_logout(self):
        from services.supabase.supabase_auth import sign_out

        self.sidebar.profile.logout_button.setEnabled(False)

        try:
            await sign_out()
        except Exception:
            self.sidebar.profile.logout_button.setEnabled(True)

            QMessageBox.warning(
                self,
                "Sign Out",
                "Unable to sign out. Please try again."
            )
            return

        self.reset_user_state()
        self.show_auth_ui()
        self.window_controls.raise_()

    async def restore_user_session(self):
        self.auth_view.set_loading(True)

        try:
            from services.supabase.supabase_auth import restore_session

            response = await restore_session()

            if response is not None and response.user is not None:
                await self.on_authenticated(response.user)

        except Exception as error:
            print(f"Session restore failed: {error}")

        finally:
            if self.page_manager is None and not self._closing:
                self.auth_view.set_loading(False)

    def position_window_controls(self):
        self.window_controls.move(
            self.width() - self.window_controls.width(),
            0
        )
        self.window_controls.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if hasattr(self, "window_controls"):
            self.position_window_controls()

    def closeEvent(self, event):
        self._closing = True
        self.usb_timer.stop()

        if self.update_worker and self.update_worker.isRunning():
            event.ignore()
            return

        super().closeEvent(event)