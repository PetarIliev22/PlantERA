import qtawesome as qta
from ui.PySide6_Qt import *


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
        layout.setContentsMargins(24, 0, 0, 0)
        layout.setSpacing(0)

        logo = QFrame()
        logo.setObjectName("toolbarLogo")
        logo.setFixedSize(56, 56)

        layout.addWidget(
            logo,
            0,
            Qt.AlignmentFlag.AlignVCenter
        )

        layout.addSpacing(16)

        title_frame = QFrame()
        title_frame.setObjectName("toolbarTitleFrame")

        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)

        title = QLabel("PlantERA - Provisioning Tool")
        title.setObjectName("toolbarTitle")

        subtitle = QLabel("Prepare. Secure. Grow.")
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
            ("maximize", "fa6s.window-maximize", self.toggle_maximize),
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
            self.toggle_maximize()

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            QTimer.singleShot(50, self.parent.round_corners)
        else:
            self.parent.remove_round_corners()
            self.parent.showMaximized()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.bottom_line.setGeometry(
            0,
            self.height() - 2,
            self.width(),
            2
        )