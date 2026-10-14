from ui.PySide6_Qt import *
from ui.components.toolbar import Toolbar
from ui.components.sidebar import Sidebar
from core.page_manager import PageManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("mainWindow")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        screen = self.screen().availableGeometry()

        self.setMinimumSize(800, 550)

        width = min(1550, int(screen.width() * 0.9))
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

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.toolbar = Toolbar(self)
        main_layout.addWidget(self.toolbar)

        content = QWidget()
        content.setObjectName("mainContent")

        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar = Sidebar(self)
        self.page_manager = PageManager(content)

        self.sidebar.page_changed.connect(
            self.page_manager.change_page
        )

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.page_manager, 1)

        main_layout.addWidget(content, 1)

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
            