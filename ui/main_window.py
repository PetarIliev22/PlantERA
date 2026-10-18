import sys
from ctypes import wintypes

from ui.PySide6_Qt import *
from ui.components.toolbar import Toolbar
from ui.components.sidebar import Sidebar
from core.page_manager import PageManager
from ui.views.provision_view import ProvisionView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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

        self.create_ui()
        
    
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
                QTimer.singleShot(
                    300,
                    self.on_usb_changed
                )

        return super().nativeEvent(eventType, message)


    def on_usb_changed(self):
        for page in self.page_manager.pages.values():
            if isinstance(page, ProvisionView):
                page.device_connection.refresh_ports()
                break
