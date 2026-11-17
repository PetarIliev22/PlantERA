from ui.common.PySide6_Qt import *
from PySide6.QtWidgets import QLineEdit, QCheckBox
from PySide6.QtGui import QAction, QIcon
from utils.svg_icons import svg_icon
from utils.paths import resource_path

class Login(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 4)
        layout.setSpacing(0)

        self.email = self.create_field(layout, "Email Address", "Enter your email")
        layout.addSpacing(12)

        self.password = self.create_field(layout, "Password", "Enter your password", True)
        layout.addSpacing(14)

        options = QHBoxLayout()

        self.remember = QCheckBox("Remember me")
        self.remember.setObjectName("authRemember")
        self.remember.setChecked(True)

        self.forgot_button = QPushButton("Forgot password?")
        self.forgot_button.setObjectName("authLink")
        self.forgot_button.setCursor(Qt.CursorShape.PointingHandCursor)

        options.addWidget(self.remember)
        options.addStretch()
        options.addWidget(self.forgot_button)

        layout.addLayout(options)
        layout.addSpacing(22)

        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("authSubmit")
        self.login_button.setFixedHeight(48)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(self.login_button)

    def create_field(self, layout, label_text, placeholder, password=False):
        container = QWidget()
        container.setObjectName("authField")

        field_layout = QVBoxLayout(container)
        field_layout.setContentsMargins(0, 0, 0, 0)
        field_layout.setSpacing(3)

        label = QLabel(label_text)
        label.setObjectName("authFieldLabel")

        field = QLineEdit()
        field.setObjectName("authInput")
        field.setPlaceholderText(placeholder)
        field.setFixedHeight(44)

        if password:
            field.setEchoMode(QLineEdit.EchoMode.Password)

            eye = svg_icon("eye.svg", "#8492A6", 18)
            eye_off = svg_icon("eye-off.svg", "#8492A6", 18)

            toggle = QAction(eye_off, "", field)
            toggle.setCheckable(True)

            def toggle_password(checked):
                field.setEchoMode(
                    QLineEdit.EchoMode.Normal if checked
                    else QLineEdit.EchoMode.Password
                )
                toggle.setIcon(eye if checked else eye_off)

            toggle.toggled.connect(toggle_password)
            field.addAction(toggle, QLineEdit.ActionPosition.TrailingPosition)
        else:
            field.setClearButtonEnabled(True)

        field_layout.addWidget(label)
        field_layout.addWidget(field)
        layout.addWidget(container)

        return field
