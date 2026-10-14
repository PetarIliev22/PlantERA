from ui.PySide6_Qt import *

def apply_shadow(widget):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(24)
    shadow.setXOffset(0)
    shadow.setYOffset(5)
    shadow.setColor(QColor(35, 55, 85, 35))
    widget.setGraphicsEffect(shadow)