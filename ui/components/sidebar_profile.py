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
        self.avatar.setFixedSize(47, 47)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.name = QLabel()
        self.name.setObjectName("profileName")

        self.role = QLabel()
        self.role.setObjectName("profileRole")

        details = QVBoxLayout()
        details.setSpacing(3)
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
                size = self.avatar.size()

                pixmap = pixmap.scaled(
                    size,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )

                result = QPixmap(size)
                result.fill(Qt.GlobalColor.transparent)

                path = QPainterPath()
                path.addEllipse(QRectF(result.rect()))

                x = (result.width() - pixmap.width()) // 2
                y = (result.height() - pixmap.height()) // 2

                painter = QPainter(result)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.setClipPath(path)
                painter.drawPixmap(x, y, pixmap)
                painter.end()

                self.avatar.setPixmap(result)
                return

        initials = "".join(
            part[0].upper() for part in name.split()[:2]
        )

        self.avatar.clear()
        self.avatar.setText(initials or "?")