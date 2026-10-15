
import qtawesome as qta
from ui.PySide6_Qt import *
from config.config_loader import load_config

sidebar = load_config("sidebar.json")["sidebar"]


class Sidebar(QFrame):
    page_changed = Signal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.active_name = sidebar[0]["name"] if sidebar else None

        self.setObjectName("sidebar")
        self.setFixedWidth(215)
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 10, 15, 20)
        layout.setSpacing(10)

        self.indicator = QFrame(self)
        self.indicator.setObjectName("activeIndicator")
        self.indicator.setGeometry(0, 10, 4, 54)

        self.buttons = {}
        self.items = {}

        for item in sidebar:
            name = item["name"]
            active = name == self.active_name

            button = QPushButton("  " + item["text"], self)

            button.setObjectName("sidebarButton")
            button.setProperty("active", active)
            button.setFixedHeight(54)

            button.setIcon(
                qta.icon(
                    item["icon"],
                    color="#FFFFFF" if active else "#D5E1F0"
                )
            )

            button.setIconSize(QSize(20, 20))
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            button.clicked.connect(
                lambda checked=False, page=name: self.set_active(page)
            )

            self.buttons[name] = button
            self.items[name] = item

            layout.addWidget(button)

        layout.addStretch()

        footer = QLabel("© 2026 Plantera Software")
        footer.setObjectName("sidebarFooter")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(footer)

        self.indicator.raise_()

    def set_active(self, name):
        if name not in self.buttons:
            return

        if name == self.active_name:
            return

        self.active_name = name

        for page_name, button in self.buttons.items():
            active = page_name == name

            button.setProperty("active", active)
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()

            button.setIcon(
                qta.icon(
                    self.items[page_name]["icon"],
                    color="#FFFFFF" if active else "#D5E1F0"
                )
            )

        self.indicator.move(
            0,
            self.buttons[name].mapTo(self, QPoint(0, 0)).y()
        )

        self.page_changed.emit(name)
