from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QWidget

class LoadingSpinner(QWidget):
    def __init__(self, size=76, color="#1687F8", parent=None):
        super().__init__(parent)

        self._angle = 0
        self.color = QColor(color)
        self.setFixedSize(size, size)

        self.animation = QPropertyAnimation(self, b"angle", self)
        self.animation.setDuration(1100)
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setLoopCount(-1)
        self.animation.setEasingCurve(QEasingCurve.Type.Linear)

    def get_angle(self):
        return self._angle

    def set_angle(self, angle):
        self._angle = angle
        self.update()

    angle = Property(int, get_angle, set_angle)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        size = min(self.width(), self.height())
        thickness = max(4, size // 10)
        margin = thickness / 2 + 3

        rect = self.rect().toRectF().adjusted(
            margin, margin, -margin, -margin
        )

        # Light gray background ring
        background_pen = QPen(QColor("#DFE7F1"), thickness)
        background_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(background_pen)
        painter.drawEllipse(rect)

        # Blue rotating arc
        arc_pen = QPen(self.color, thickness)
        arc_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(arc_pen)
        painter.drawArc(
            rect,
            int((90 - self._angle) * 16),
            -80 * 16
        )

        painter.end()

    def start(self):
        self.animation.start()

    def stop(self):
        self.animation.stop()
