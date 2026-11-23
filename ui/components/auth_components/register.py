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
