from ui.PySide6_Qt import *
from utils.paths import resource_path
from config.config_loader import load_config
from ui.components.sidebar_profile import SidebarProfile

sidebar = load_config("sidebar.json")["sidebar"]

class Sidebar(QFrame):
    page_changed = Signal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.active_name = sidebar[0]["name"] if sidebar else None

        self.setObjectName("sidebar")
        self.setFixedWidth(260)
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 20)
        layout.setSpacing(10)

        logo = QLabel()
        logo.setObjectName("sidebarLogo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setFixedHeight(90)

        pixmap = QPixmap(
            str(resource_path(
                "assets", "img", "logo", "plantera_white_logo.png"
            ))
        )

        dpr = logo.devicePixelRatioF()
        scaled = pixmap.scaled(
            round(210 * dpr),
            round(90 * dpr),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        scaled.setDevicePixelRatio(dpr)
        logo.setPixmap(scaled)

        layout.addWidget(logo)
        layout.addSpacing(20)
            
        self.indicator = QFrame(self)
        self.indicator.setObjectName("activeIndicator")
        self.indicator.setGeometry(0, 118, 4, 54)

        self.buttons = {}

        for item in sidebar:
            name = item["name"]
            active = name == self.active_name

            button = QPushButton("  " + item["text"], self)

            button.setObjectName("sidebarButton")
            button.setProperty("active", active)
            button.setFixedHeight(54)

            button.setIcon(
                self.get_icon(item["icon"])
            )

            button.setIconSize(QSize(20, 20))
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            button.clicked.connect(
                lambda checked=False, page=name: self.set_active(page)
            )

            self.buttons[name] = button

            layout.addWidget(button)

        layout.addStretch()
        self.profile = SidebarProfile(self)
        layout.addWidget(self.profile)
        layout.addSpacing(10)
        
        footer = QLabel("© 2026 Plantera Software")
        footer.setObjectName("sidebarFooter")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(footer)

        self.indicator.raise_()

    def get_icon(self, icon_name):
        return QIcon(
            str(resource_path("assets", "img", "icons", icon_name))
        )

    def update_button(self, name, active):
        button = self.buttons[name]

        button.setProperty("active", active)
        button.style().unpolish(button)
        button.style().polish(button)
        button.update()

    def set_active(self, name):
        if name not in self.buttons:
            return

        if name == self.active_name:
            return

        if self.active_name in self.buttons:
            self.update_button(self.active_name, False)

        self.active_name = name
        self.update_button(name, True)

        self.indicator.move(
            0,
            self.buttons[name].mapTo(self, QPoint(0, 0)).y()
        )

        self.page_changed.emit(name)
        
