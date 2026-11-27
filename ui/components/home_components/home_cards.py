from ui.common.PySide6_Qt import *
from utils.svg_icons import svg_icon
from utils.shadow import apply_shadow
from config.config_loader import load_config

cards_config = load_config("home.json")["cards"]

class HomeCards(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(24)

        self.create_ui()

    def create_ui(self):
        for item in cards_config:
            self.addWidget(
                self.create_card(item["icon"], item["title"], item["description"]),
                1
            )

    def create_card(self, icon_name, title, description):
        card = QFrame()
        card.setObjectName("homeCard")

        layout = QHBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        icon = QLabel()
        icon.setObjectName("homeCardIcon")
        icon.setFixedSize(44, 44)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setPixmap(svg_icon(icon_name, "#1687F8", 22).pixmap(22, 22))

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(5)

        for name, text in (
            ("homeCardTitle", title),
            ("homeCardDescription", description)
        ):
            label = QLabel(text)
            label.setObjectName(name)
            label.setTextFormat(Qt.TextFormat.PlainText)
            label.setWordWrap(True)
            text_layout.addWidget(label)

        layout.addWidget(icon, 0, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(text_layout, 1)

        apply_shadow(card)

        return card