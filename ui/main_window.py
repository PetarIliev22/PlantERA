import sys
from ctypes import wintypes

from ui.PySide6_Qt import *
from ui.components.toolbar import Toolbar
from ui.components.sidebar import Sidebar
from core.page_manager import PageManager
from ui.views.provision_view import ProvisionView
from services.update_worker import UpdateWorker
from ui.dialogs.update_dialog import show_update_dialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._closing = False
        
        self.setObjectName("mainWindow")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        screen = self.screen().availableGeometry()

        self.setMinimumSize(800, 550)

        width = min(1650, int(screen.width() * 0.95))
        height = min(900, int(screen.height() * 0.9))

        self.resize(width, height)

        self.move(
            screen.x() + (screen.width() - width) // 2,
            screen.y() + (screen.height() - height) // 2
        )

        self.usb_timer = QTimer(self)
        self.usb_timer.setSingleShot(True)
        self.usb_timer.setInterval(300)
        self.usb_timer.timeout.connect(self.on_usb_changed)
        
        self.create_ui()
        
        self.update_worker = UpdateWorker(
            download=False,
            update=self.update,
            parent=self
        )

        self.update_worker.update_available.connect(
            self.on_update_available
        )

        self.update_worker.finished.connect(
            self.on_update_check_finished
        )

        self.update_worker.start()
        
    def create_ui(self):
        central = QWidget()
        central.setObjectName("mainContainer")
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar(self)
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
        
    def round_corners(self):
        path = QPainterPath()
        path.addRoundedRect(
            QRectF(self.rect()),
            20,
            20
        )

        self.setMask(
            QRegion(
                path.toFillPolygon().toPolygon()
            )
        )

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
            
    def nativeEvent(self, eventType, message):
        if sys.platform == "win32":
            msg = wintypes.MSG.from_address(int(message))

            if (
                msg.message == 0x0219
                and msg.wParam in (0x0007, 0x8000, 0x8004)
            ):
                
                self.usb_timer.start()

        return super().nativeEvent(eventType, message)


    def on_usb_changed(self):
        provision = self.page_manager.pages.get("provision")

        if isinstance(provision, ProvisionView):
            provision.device_connection.refresh_ports()
            
    
    def on_update_available(self, update):
        if self._closing:
            return

        self.update_dialog = show_update_dialog(self, update)


    def on_update_check_finished(self):
        if self._closing:
            QTimer.singleShot(0, self.close)


    def closeEvent(self, event):
        self._closing = True

        if self.update_worker.isRunning():
            event.ignore()
            return

        super().closeEvent(event)

