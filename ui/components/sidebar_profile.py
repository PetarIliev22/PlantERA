from ui.common.PySide6_Qt import *

class SidebarProfile(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("sidebarProfile")
        self.setFixedHeight(65)

        self.create_ui()

    def create_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        self.avatar = QLabel("?")
        self.avatar.setObjectName("profileAvatar")
        self.avatar.setFixedSize(44, 44)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.name = QLabel()
        self.name.setObjectName("profileName")

        self.role = QLabel()
        self.role.setObjectName("profileRole")

        details = QVBoxLayout()
        details.setSpacing(0)
        details.setContentsMargins(0, 0, 0, 0)

        details.addStretch()
        details.addWidget(self.name)
        details.addWidget(self.role)
        details.addStretch()

        layout.addWidget(self.avatar)
        layout.addLayout(details, 1)

    def set_profile(self, profile, image_data=None):
        name = f"{profile['first_name']} {profile['last_name']}".strip()

        self.name.setText(name)
        self.role.setText(profile["role"].capitalize())

        if image_data:
            pixmap = QPixmap()

            if pixmap.loadFromData(image_data):
                self.avatar.setPixmap(
                    pixmap.scaled(
                        self.avatar.size(),
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )
                return

        initials = "".join(
            part[0].upper() for part in name.split()[:2]
        )

        self.avatar.clear()
        self.avatar.setText(initials or "?")