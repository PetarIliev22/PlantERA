from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainterPath, QRegion

class WindowAppearance:
    def setup_window(self):
        self.setObjectName("mainWindow")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(800, 550)

        screen = self.screen().availableGeometry()

        width = min(1650, int(screen.width() * 0.95))
        height = min(900, int(screen.height() * 0.9))

        self.resize(width, height)
        self.move(
            screen.x() + (screen.width() - width) // 2,
            screen.y() + (screen.height() - height) // 2
        )

    def round_corners(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)
        self.setMask(QRegion(path.toFillPolygon().toPolygon()))

    def remove_round_corners(self):
        self.clearMask()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self.isMaximized():
            self.remove_round_corners()
        else:
            self.round_corners()

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
