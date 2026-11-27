from qasync import asyncClose
from ui.common.PySide6_Qt import *
from ui.components.window_controls import WindowControls

from .window_events import WindowEvents
from .window_appearance import WindowAppearance
from .window_updates import WindowUpdates
from .window_auth import WindowAuth
from .window_ui import WindowUI
from .window_realtime import WindowRealtime

class MainWindow(
    WindowEvents,
    WindowAppearance,
    WindowUpdates,
    WindowAuth,
    WindowUI,
    WindowRealtime,
    QMainWindow
):
    def __init__(self):
        super().__init__()

        self.realtime = None
        self._closing = False
        self.update_worker = None

        self.reset_user_state()
        self.setup_window()
        self.setup_timers()
        self.show_auth_ui()

        self.window_controls = WindowControls(self)
        self.window_controls.show()

        self.position_window_controls()

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

    @asyncClose
    async def closeEvent(self, event):
        if self.update_worker and self.update_worker.isRunning():
            event.ignore()
            return

        self._closing = True
        self.usb_timer.stop()

        await self.stop_realtime()

        super().closeEvent(event)