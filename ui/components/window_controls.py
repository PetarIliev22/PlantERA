from ui.common.PySide6_Qt import *
from utils.paths import resource_path

class WindowControls(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 12, 0)
        layout.setSpacing(0)

        buttons = [
            ("minimize", "minimize.svg", parent.showMinimized),
            ("maximize", "maximize.svg", parent.toggle_maximize),
            ("close", "close.svg", parent.close),
        ]

        for name, icon, command in buttons:
            button = QPushButton(self)
            button.setObjectName(f"{name}Button")
            button.setFixedSize(44, 36)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setIcon(
                QIcon(str(resource_path("assets", "img", "icons", icon)))
            )
            button.setIconSize(QSize(15, 15))
            button.clicked.connect(command)

            layout.addWidget(button)

        self.setFixedSize(144, 36)
