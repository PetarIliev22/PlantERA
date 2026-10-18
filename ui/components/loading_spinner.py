
from PySide6.QtCore import Qt, Property, QPropertyAnimation
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QWidget

class LoadingSpinner(QWidget):
    def __init__(self, size=42, color="#1687F8", parent=None):
        super().__init__(parent)

        self._angle = 0
        self.color = QColor(color)
        self.setFixedSize(size, size)

        self.animation = QPropertyAnimation(self, b"angle", self)
        self.animation.setDuration(1200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(359)
        self.animation.setLoopCount(-1)

    def get_angle(self):
        return self._angle

    def set_angle(self, angle):
        self._angle = angle
        self.update()

    angle = Property(int, get_angle, set_angle)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self._angle)

        pen = QPen(self.color, max(3, self.width() // 11))
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        radius = self.width() // 2 - pen.width() - 2

        painter.drawArc(
            -radius, -radius,
            radius * 2, radius * 2,
            0, 270 * 16
        )

    def start(self):
        self.animation.start()

    def stop(self):
        self.animation.stop()
