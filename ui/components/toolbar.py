from ui.PySide6_Qt import *
from utils.paths import resource_path

class Toolbar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.window()
        self.drag_position = QPoint()

        self.setObjectName("toolbar")
        self.setFixedHeight(86)

        self.create_ui()

    def create_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 0, 12, 0)
        layout.setSpacing(0)

        title_frame = QFrame()
        title_frame.setObjectName("toolbarTitleFrame")

        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)

        title = QLabel("Device Provisioning")
        title.setObjectName("toolbarTitle")

        subtitle = QLabel("Secure Device Configuration & Management")
        subtitle.setObjectName("toolbarSubtitle")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        layout.addWidget(
            title_frame,
            0,
            Qt.AlignmentFlag.AlignVCenter
        )

        layout.addStretch()
        
        buttons = [
            ("minimize", "minimize.svg", self.window().showMinimized),
            ("maximize", "maximize.svg", self.window().showMaximized),
            ("close", "close.svg", self.window().close),
        ]

        for name, icon, command in buttons:
            button = QPushButton()
            button.setObjectName(f"{name}Button")
            button.setFixedSize(44, 36)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setIcon(
                QIcon(str(resource_path("assets","img", "icons", icon)))
            )
            button.setIconSize(QSize(18, 18))
            button.clicked.connect(command)

            layout.addWidget(
                button,
                0,
                Qt.AlignmentFlag.AlignTop
            )

        self.bottom_line = QFrame(self)
        self.bottom_line.setObjectName("toolbarBottomLine")
        self.bottom_line.setFixedHeight(2)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.window().frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if (
            event.buttons() & Qt.MouseButton.LeftButton
            and not self.window().isMaximized()
        ):
            new_pos = (
                event.globalPosition().toPoint()
                - self.drag_position
            )

            screen = self.window().screen().availableGeometry()

            x = max(
                screen.left(),
                min(new_pos.x(), screen.right() - self.window().width() + 1)
            )

            y = max(
                screen.top(),
                min(new_pos.y(), screen.bottom() - self.window().height() + 1)
            )

            self.window().move(x, y)
            

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.window().toggle_maximize()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.bottom_line.setGeometry(
            0,
            self.height() - 2,
            self.width(),
            2
        )