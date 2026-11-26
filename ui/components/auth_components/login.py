from ui.common.PySide6_Qt import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, Qt
from PySide6.QtWidgets import QCheckBox
from ui.components.auth_components.auth_field import create_auth_field

class Login(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 4)
        layout.setSpacing(0)

        self.email = create_auth_field(layout, "Email Address", "Enter your email")
        layout.addSpacing(12)

        self.password = create_auth_field(layout, "Password", "Enter your password", True)
        layout.addSpacing(14)

        options = QHBoxLayout()

        # TODO : ---
        self.remember = QCheckBox("Remember me")
        self.remember.setObjectName("authRemember")
        self.remember.setChecked(False)

        # self.forgot_button = QPushButton("Forgot password?")
        # self.forgot_button.setObjectName("authLink")
        # self.forgot_button.setCursor(Qt.CursorShape.PointingHandCursor)

        options.addWidget(self.remember)
        options.addStretch()
        # options.addWidget(self.forgot_button)

        layout.addLayout(options)
        layout.addSpacing(22)

    