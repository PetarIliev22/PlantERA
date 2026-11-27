from ui.common.PySide6_Qt import QWidget, QVBoxLayout, QLabel, QPushButton, Qt, Signal
from utils.svg_icons import svg_icon

class BlockedLogin(QWidget):
    back_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setObjectName("authBlockedContainer")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedWidth(480)
        
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(12)

        icon = QLabel()
        icon.setObjectName("authBlockedIcon")
        icon.setFixedSize(96, 96)
        icon.setPixmap(
            svg_icon("lock.svg", "#EF4444", 48).pixmap(48, 48)
        )

        title = QLabel("Account blocked")
        title.setObjectName("authBlockedTitle")

        description = QLabel(
            "Your account has been blocked by an administrator. "
            "Please contact your administrator to restore access."
        )
        description.setObjectName("authBlockedDescription")
        description.setFixedWidth(380)
        description.setWordWrap(True)

        for widget in (icon, title, description):
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.back_button = QPushButton("Back to login")
        self.back_button.setObjectName("authBlockButton")
        self.back_button.setFixedHeight(48)
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.clicked.connect(self.back_requested.emit)

        layout.addWidget(self.back_button)