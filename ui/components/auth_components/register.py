from ui.common.PySide6_Qt import *
from ui.components.auth_components.login import Login

class Register(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 4)
        layout.setSpacing(0)

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

        self.register_button = QPushButton("Create Account")
        self.register_button.setObjectName("authSubmit")
        self.register_button.setFixedHeight(44)
        self.register_button.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(self.register_button)
