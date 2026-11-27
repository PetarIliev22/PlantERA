from ui.common.PySide6_Qt import *


class Toolbar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.drag_position = QPoint()

        self.setObjectName("toolbar")
        self.setFixedHeight(86)

        self.create_ui()

    def create_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 0, 12, 0)
        layout.setSpacing(0)
        layout.addStretch()

        self.bottom_line = QFrame(self)
        self.bottom_line.setObjectName("toolbarBottomLine")
        self.bottom_line.setFixedHeight(2)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            window = self.window()
            self.drag_position = (
                event.globalPosition().toPoint()
                - window.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        window = self.window()

        if window.isMaximized():
            return

        if not event.buttons() & Qt.MouseButton.LeftButton:
            return

        position = event.globalPosition().toPoint() - self.drag_position
        screen = window.screen().availableGeometry()

        max_x = screen.right() - window.width() + 1
        max_y = screen.bottom() - window.height() + 1

        x = max(screen.left(), min(position.x(), max_x))
        y = max(screen.top(), min(position.y(), max_y))

        window.move(x, y)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.window().toggle_maximize()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.bottom_line.resize(self.width(), 2)
        self.bottom_line.move(0, self.height() - 2)