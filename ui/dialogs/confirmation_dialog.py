from ui.common.PySide6_Qt import *
from utils.svg_icons import svg_icon
from utils.overlay import show_overlay, remove_overlay

ACTIONS = {
    "Block": (
        "lock.svg", "#D97706",
        "This user will no longer be able to access PlantERA after signing out."
    ),
    "Unblock": (
        "unlock.svg", "#16A34A",
        "This user will regain access to PlantERA."
    ),
    "Delete": (
        "trash.svg", "#DC2626",
        "This user will be permanently deleted. This action cannot be undone."
    )
}

class ConfirmationDialog(QDialog):
    def __init__(self, action, user, parent=None):
        super().__init__(parent)
        self.overlay = None

        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedWidth(420)

        self.create_ui(action, user)

    def create_ui(self, action, user):
        icon_name, color, message = ACTIONS[action]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        container = QFrame()
        container.setObjectName("confirmationContainer")

        content = QVBoxLayout(container)
        content.setContentsMargins(28, 28, 28, 28)
        content.setSpacing(16)

        icon = QLabel()
        icon.setObjectName("confirmationIcon")
        icon.setFixedSize(72, 72)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setPixmap(svg_icon(icon_name, color, 30).pixmap(30, 30))

        title = QLabel(f"{action} User")
        title.setObjectName("confirmationTitle")

        description = QLabel(message)
        description.setObjectName("confirmationDescription")
        description.setWordWrap(True)

        for widget in (title, description):
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content.addWidget(icon, 0, Qt.AlignmentFlag.AlignCenter)
        content.addWidget(title)
        content.addWidget(description)
        content.addWidget(self.create_user_info(user))
        content.addLayout(self.create_buttons(action))

        layout.addWidget(container)

    def create_user_info(self, user):
        container = QFrame()
        container.setObjectName("confirmationUser")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(4)

        name = f"{user['first_name']} {user['last_name']}".strip()

        for text, object_name in (
            (name, "confirmationUserName"),
            (user["email"], "confirmationUserEmail")
        ):
            label = QLabel(text)
            label.setObjectName(object_name)
            label.setTextFormat(Qt.TextFormat.PlainText)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setWordWrap(True)
            layout.addWidget(label)

        return container

    def create_buttons(self, action):
        layout = QHBoxLayout()
        layout.setSpacing(12)

        cancel = QPushButton("Cancel")
        cancel.setObjectName("confirmationCancel")
        cancel.clicked.connect(self.reject)

        confirm = QPushButton(f"{action} User")
        confirm.setObjectName("confirmationSubmit")
        confirm.setProperty("action", action.lower())
        confirm.clicked.connect(self.accept)

        for button in (cancel, confirm):
            button.setFixedHeight(44)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setAutoDefault(False)
            layout.addWidget(button, 1)

        cancel.setDefault(True)
        cancel.setFocus()

        return layout
    
    def showEvent(self, event):
        super().showEvent(event)

        if self.overlay is None and self.parentWidget():
            self.overlay = show_overlay(self.parentWidget().window())

        self.raise_()

    def hideEvent(self, event):
        remove_overlay(self.overlay)
        self.overlay = None

        super().hideEvent(event)