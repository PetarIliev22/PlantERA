import sys
from ctypes import wintypes
from ui.common.PySide6_Qt import *
from ui.components.toolbar import Toolbar
from ui.components.sidebar import Sidebar
from ui.views.auth_views import AuthView
from core.page_manager import PageManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._closing = False

        self.setup_window()
        self.setup_timers()
        self.create_ui()
        self.start_update_check()

    # Window setup
    def setup_window(self):
        self.setObjectName("mainWindow")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(800, 550)

        screen = self.screen().availableGeometry()

        width = min(1650, int(screen.width() * 0.95))
        height = min(900, int(screen.height() * 0.9))

        self.resize(width, height)
        self.move(
            screen.x() + (screen.width() - width) // 2,
            screen.y() + (screen.height() - height) // 2
        )

    # Timers
    def setup_timers(self):
        self.usb_timer = QTimer(self)
        self.usb_timer.setSingleShot(True)
        self.usb_timer.setInterval(300)
        self.usb_timer.timeout.connect(self.on_usb_changed)

    # User interface
    def create_ui(self):
        self.auth_view = AuthView(self)
        self.setCentralWidget(self.auth_view)

    # Updates
    def start_update_check(self):
        from services.updates.update_worker import UpdateWorker

        self.update_worker = UpdateWorker(
            download=False,
            parent=self
        )

        self.update_worker.update_available.connect(
            self.on_update_available
        )
        self.update_worker.finished.connect(
            self.on_update_check_finished
        )

        self.update_worker.start()

    def on_update_available(self, update):
        if self._closing:
            return

        from ui.dialogs.update_dialog import show_update_dialog
        self.update_dialog = show_update_dialog(self, update)

    def on_update_check_finished(self):
        if self._closing:
            QTimer.singleShot(0, self.close)

    # USB devices
    def on_usb_changed(self):
        if not hasattr(self, "page_manager"):
            return

        provision = self.page_manager.pages.get("provision")

        if provision is not None:
            provision.device_connection.refresh_ports()

    def nativeEvent(self, eventType, message):
        if sys.platform == "win32":
            msg = wintypes.MSG.from_address(int(message))

            if (
                msg.message == 0x0219
                and msg.wParam in (0x0007, 0x8000, 0x8004)
            ):
                self.usb_timer.start()

        return super().nativeEvent(eventType, message)

    # Window appearance
    def round_corners(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))

    def remove_round_corners(self):
        self.clearMask()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self.isMaximized():
            self.remove_round_corners()
        else:
            self.round_corners()

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # Closing
    def closeEvent(self, event):
        self._closing = True
        self.usb_timer.stop()

        if self.update_worker.isRunning():
            event.ignore()
            return

        super().closeEvent(event)
