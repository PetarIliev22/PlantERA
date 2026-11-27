from ui.common.PySide6_Qt import *
from ui.components.home_components.home_banner import HomeBanner
from ui.components.home_components.home_cards import HomeCards

class HomeView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("homeView")
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        layout.addWidget(HomeBanner(self))
        layout.addLayout(HomeCards())
        layout.addStretch()