import qtawesome as qta
from ui.PySide6_Qt import *
from config.config_loader import load_config

sidebar = load_config("sidebar.json")["sidebar"]

class Sidebar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName("sidebar")
        self.setFixedWidth(250)
        self.active_name = "provision"
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
            
            # TODO: MAKE THIS DYNAMIC
            active = item["name"] == self.active_name
            button = QPushButton(item["text"], self)

            button.setObjectName("sidebarButton")
            button.setProperty("active", active)
            button.setFixedHeight(54)

            button.setIcon(
                qta.icon(
                    item["icon"],
                    color="#1687F8" if active else "#8491A5"
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