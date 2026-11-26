from ui.common.PySide6_Qt import QWidget, QVBoxLayout, QLabel, QPushButton, QPixmap, Qt
from PySide6.QtGui import QPainter, QPainterPath

class RememberedLogin(QWidget):
    def __init__(self, profile, parent=None):
        super().__init__(parent)

        self.profile = profile
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 4)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.avatar = QLabel()
        self.avatar.setObjectName("authAvatar")
        self.avatar.setFixedSize(96, 96)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        avatar = self.profile.get("avatar")

        if avatar:
            pixmap = QPixmap()

            if pixmap.loadFromData(avatar):
                pixmap = pixmap.scaled(
                    92, 92,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )

                rounded = QPixmap(92, 92)
                rounded.fill(Qt.GlobalColor.transparent)

                painter = QPainter(rounded)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)

                path = QPainterPath()
                path.addEllipse(0, 0, 92, 92)

                painter.setClipPath(path)
                painter.drawPixmap(
                    (92 - pixmap.width()) // 2,
                    (92 - pixmap.height()) // 2,
                    pixmap
                )
                painter.end()

                self.avatar.setPixmap(rounded)

        self.full_name = QLabel(
            f"{self.profile['first_name']} {self.profile['last_name']}"
        )
        self.full_name.setObjectName("authProfileName")

        self.email = QLabel(self.profile["email"])
        self.email.setObjectName("authProfileEmail")

        for widget in (
            self.avatar,
            self.full_name,
            self.email
        ):
            layout.addWidget(
                widget,
                alignment=Qt.AlignmentFlag.AlignCenter
            )