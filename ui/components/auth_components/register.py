from ui.common.PySide6_Qt import *
from ui.components.auth_components.login import Login
from utils.svg_icons import svg_icon

class Register(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.avatar_path = None
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 4)
        layout.setSpacing(0)
        
        photo_layout = QHBoxLayout()
        photo_layout.setSpacing(16)

        self.avatar = QLabel()
        self.avatar.setObjectName("registerAvatar")
        self.avatar.setFixedSize(76, 76)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.avatar_icon = svg_icon("user.svg", "#94a3b8", 36)
        self.avatar.setPixmap(self.avatar_icon.pixmap(36, 36))

        photo_title = QLabel("Profile Photo (Optional)")
        photo_title.setObjectName("photoTitle")

        self.photo_button = QPushButton("Upload Photo")
        self.photo_button.setObjectName("uploadPhotoButton")
        self.photo_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.photo_button.clicked.connect(self.select_photo)

        self.remove_button = QPushButton("Remove")
        self.remove_button.setObjectName("removePhotoButton")
        self.remove_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.remove_button.clicked.connect(self.remove_photo)
        self.remove_button.hide()

        photo_hint = QLabel("JPG, PNG or WEBP · Max 5 MB")
        photo_hint.setObjectName("photoHint")

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)
        buttons_layout.addWidget(self.photo_button)
        buttons_layout.addWidget(self.remove_button)
        buttons_layout.addStretch()

        photo_details = QVBoxLayout()
        photo_details.setSpacing(6)
        photo_details.addWidget(photo_title)
        photo_details.addLayout(buttons_layout)
        photo_details.addWidget(photo_hint)

        photo_layout.addWidget(self.avatar)
        photo_layout.addLayout(photo_details, 1)

        layout.addLayout(photo_layout)
        layout.addSpacing(22)
        
        name_layout = QHBoxLayout()
        name_layout.setSpacing(12)
        
        self.first_name = Login.create_field(
            self, name_layout, "First Name", "Enter first name"
        )

        self.last_name = Login.create_field(
            self, name_layout, "Last Name", "Enter last name"
        )
        
        layout.addLayout(name_layout)
        layout.addSpacing(18)
        
        self.email = Login.create_field(
            self, layout, "Email Address", "Enter your email"
        )
        layout.addSpacing(18)

        self.password = Login.create_field(
            self, layout, "Password", "Create a password", True
        )
        layout.addSpacing(18)

        self.confirm = Login.create_field(
            self, layout, "Confirm Password", "Repeat your password", True
        )
        layout.addSpacing(22)
         
    def remove_photo(self):
        self.avatar.setPixmap(self.avatar_icon.pixmap(36, 36))
        self.avatar_path = None
        self.remove_button.hide()
        
    def select_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            caption="Select Profile Photo",
            filter="Images (*.jpg *.jpeg *.png *.webp)"
        )

        if not file_path:
            return

        pixmap = QPixmap(file_path)

        if pixmap.isNull():
            return

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
        self.avatar_path = file_path
        
        self.remove_button.show()
        
