from ui.PySide6_Qt import *
from ui.components.toolbar import Toolbar
from ui.components.sidebar import Sidebar
from ui.views.provision_view import ProvisionView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("mainWindow")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        screen = QApplication.primaryScreen().availableGeometry()

        self.setMinimumSize(
            min(1100, int(screen.width() * 0.8)),
            min(700, int(screen.height() * 0.8))
        )

        self.resize(
            min(1550, int(screen.width() * 0.9)),
            min(900, int(screen.height() * 0.9))
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
        self.provision_view = ProvisionView(self)

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.provision_view, 1)

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
                