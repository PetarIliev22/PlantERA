import json
import qtawesome as qta
from ui.PySide6_Qt import *

sidebar = json.load(
    open("config/sidebar.json", encoding="utf-8")
)["sidebar"]

class Sidebar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName("sidebar")
        self.setFixedWidth(250)

        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 20)
        layout.setSpacing(10)

        indicator = QFrame(self)
        indicator.setObjectName("activeIndicator")
        indicator.setGeometry(0, 5, 8, 54)

        self.buttons = {}

        for item in sidebar:
            button = QPushButton(item["text"], self)

            button.setObjectName("sidebarButton")
            button.setProperty("active", item["active"])
            button.setFixedHeight(54)

            button.setIcon(
                qta.icon(
                    item["icon"],
                    color="#1687F8" if item["active"] else "#8491A5"
                )
            )

            button.setIconSize(QSize(20, 20))
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            self.buttons[item["name"]] = button
            layout.addWidget(button)

        layout.addStretch()

        footer = QLabel("© 2026 Plantera Software")
        footer.setObjectName("sidebarFooter")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(footer)