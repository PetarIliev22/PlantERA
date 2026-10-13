import qtawesome as qta
from ui.PySide6_Qt import *
from utils.paths import resource_path

class Toolbar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.drag_position = QPoint()

        self.setObjectName("toolbar")
        self.setFixedHeight(80)

        self.create_ui()

    def create_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(40, 0, 0, 0)
        layout.setSpacing(0)

        logo = QLabel()
        logo.setObjectName("toolbarLogo")
        logo.setFixedSize(180, 80)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pixmap = QPixmap(str(resource_path("assets", "img", "logo", "plantera_full_logo.png")))
        
        logo.setPixmap(
            pixmap.scaled(
                230,
                80,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        layout.addWidget(
            logo,
            0,
            Qt.AlignmentFlag.AlignVCenter
        )

        layout.addSpacing(16)

        title_frame = QFrame()
        title_frame.setObjectName("toolbarTitleFrame")

        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(50, 0, 0, 0)
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
            ("minimize", "fa6s.window-minimize", self.parent.showMinimized),
            ("maximize", "fa6s.window-maximize", self.parent.toggle_maximize),
            ("close", "fa6s.xmark", self.parent.close),
        ]

        for name, icon, command in buttons:
            button = QPushButton()
            button.setObjectName(f"{name}Button")
            button.setFixedSize(50, 35)
            button.setIcon(qta.icon(icon, color="#8491A5"))
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
                - self.parent.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if (
            event.buttons() & Qt.MouseButton.LeftButton
            and not self.parent.isMaximized()
        ):
            self.parent.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent.toggle_maximize()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.bottom_line.setGeometry(
            0,
            self.height() - 2,
            self.width(),
            2
        )