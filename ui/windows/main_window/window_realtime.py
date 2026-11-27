import asyncio
from importlib import import_module

class WindowRealtime:
    async def start_realtime(self):
        from services.supabase.supabase_auth import get_active_session

        user = self.current_user

        if user is None or self.realtime is not None:
            return

        try:
            session = await get_active_session()

            if session is None or self.current_user is not user:
                return

            module = await asyncio.to_thread(
                import_module,
                "services.supabase.supabase_realtime"
            )

            if self.current_user is not user:
                return

            self.realtime = module.RealtimeService()

            await self.realtime.connect(session.access_token)

            if self.current_user is not user:
                await self.stop_realtime()
                return

            await self.realtime.subscribe(
                name="user_status",
                table="profiles",
                event="UPDATE",
                row_filter=f"id=eq.{user.id}",
                callback=self.on_user_status_changed
            )

        except Exception as error:
            print(f"Realtime connection failed: {error}")
            await self.stop_realtime()

    async def stop_realtime(self):
        realtime = self.realtime
        self.realtime = None

        if realtime is not None:
            try:
                await realtime.disconnect()
            except Exception as error:
                print(f"Realtime disconnect failed: {error}")

    def on_user_status_changed(self, payload):
        record = payload.get("data", {}).get("record", {})

        if self.current_user is None:
            return

        if record.get("is_blocked") is True:
            asyncio.create_task(self.handle_blocked_user())