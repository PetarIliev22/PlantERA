
from ui.PySide6_Qt import *
from utils.paths import resource_path

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

        self.avatar = QLabel("P")
        self.avatar.setObjectName("profileAvatar")
        self.avatar.setFixedSize(44, 44)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.name = QLabel("Petar Iliev")
        self.name.setObjectName("profileName")

        self.role = QLabel("Administrator")
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
    
    def set_profile(self, name, role, image_path=None):
        self.name.setText(name)
        self.role.setText(role)

        if image_path:
            pixmap = QPixmap(str(resource_path(*image_path.split("/"))))

            if not pixmap.isNull():
                self.avatar.setPixmap(
                    pixmap.scaled(
                        44,
                        44,
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )
                return

        self.avatar.setPixmap(QPixmap())
        self.avatar.setText(name[:1].upper() if name else "?")
