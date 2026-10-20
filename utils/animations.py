
from PySide6.QtCore import (
    Qt, Property, QPropertyAnimation, QEasingCurve,
)
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect

class FadeOverlay(QWidget):
    def __init__(self, parent, color="#FFFFFF"):
        super().__init__(parent)

        self._opacity = 255
        self.color = QColor(color)
        self.setGeometry(parent.rect())
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.raise_()

    def get_opacity(self):
        return self._opacity

    def set_opacity(self, value):
        self._opacity = value
        self.update()

    opacity = Property(int, get_opacity, set_opacity)

    def paintEvent(self, event):
        painter = QPainter(self)
        color = QColor(self.color)
        color.setAlpha(self._opacity)
        painter.fillRect(self.rect(), color)

def fade_in_page(widget, duration=350):
    overlay = FadeOverlay(widget)
    overlay.show()

    animation = QPropertyAnimation(overlay, b"opacity", overlay)
    animation.setDuration(duration)
    animation.setStartValue(255)
    animation.setEndValue(0)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    animation.finished.connect(overlay.deleteLater)
    overlay.animation = animation
    animation.start()

def fade_in_widget(widget, duration=300):
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b"opacity", widget)
    animation.setDuration(duration)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    widget.fade_animation = animation
    animation.start()