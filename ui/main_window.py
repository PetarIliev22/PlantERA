from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainterPath, QRegion
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)

from ui.components.toolbar import Toolbar
from ui.components.sidebar import Sidebar
from ui.views.provision_view import ProvisionView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("mainWindow")

        self.resize(1300, 800)
        self.setMinimumSize(1300, 800)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
        )

        self.create_ui()

        QTimer.singleShot(
            100,
            self.round_corners
        )

    def create_ui(self):
        self.central = QWidget()
        self.central.setObjectName("mainContainer")
        self.setCentralWidget(self.central)

        main_layout = QVBoxLayout(self.central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Toolbar
        self.toolbar = Toolbar(self)
        main_layout.addWidget(self.toolbar)

        # Content
        content = QWidget()
        content.setObjectName("mainContent")

        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.sidebar = Sidebar(self)
        content_layout.addWidget(self.sidebar)

        self.provision_view = ProvisionView(self)
        content_layout.addWidget(
            self.provision_view,
            1
        )

        main_layout.addWidget(
            content,
            1
        )

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