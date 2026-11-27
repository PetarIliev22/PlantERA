from ui.common.PySide6_Qt import *
from utils.svg_icons import svg_icon
from utils.avatar import set_avatar

class SidebarProfile(QFrame):
    logout_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("sidebarProfile")
        self.setFixedHeight(65)

        self.create_ui()

    def create_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(9, 10, 9, 10)
        layout.setSpacing(8)

        self.avatar = QLabel("?")
        self.avatar.setObjectName("profileAvatar")
        self.avatar.setFixedSize(42, 42)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.name = QLabel()
        self.name.setObjectName("profileName")

        self.role = QLabel()
        self.role.setObjectName("profileRole")

        details = QVBoxLayout()
        details.setSpacing(4)
        details.setContentsMargins(0, 0, 0, 0)

        details.addStretch()
        details.addWidget(self.name)
        details.addWidget(self.role)
        details.addStretch()

        separator = QFrame()
        separator.setObjectName("profileSeparator")
        separator.setFixedSize(1, 30)

        self.logout_button = QPushButton()
        self.logout_button.setObjectName("profileLogout")
        self.logout_button.setFixedSize(30, 32)
        self.logout_button.setIcon(
            svg_icon("log-out.svg", "#DC2626", 17)
        )
        self.logout_button.setIconSize(QSize(17, 17))
        self.logout_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logout_button.setToolTip("Sign out")

        self.logout_button.clicked.connect(
            self.logout_requested.emit
        )

        layout.addWidget(self.avatar)
        layout.addLayout(details, 1)
        layout.addWidget(separator)
        layout.addWidget(self.logout_button)

    def set_profile(self, profile, image_data=None):
        name = f"{profile['first_name']} {profile['last_name']}".strip()

        self.name.setText(name)
        self.name.setToolTip(name)
        self.role.setText(profile["role"].upper())

        set_avatar(self.avatar, profile, image_data)