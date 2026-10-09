from ui.PySide6_Qt import *
from ui.components.toolbar import Toolbar
from ui.components.sidebar import Sidebar
from ui.views.provision_view import ProvisionView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("mainWindow")
        self.resize(1400, 800)
        self.setMinimumSize(1100, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        QTimer.singleShot(100, self.round_corners)
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
        self.round_corners()