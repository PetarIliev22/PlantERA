from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

class Alert(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("appAlert")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 12, 12, 12)
        layout.setSpacing(10)

        self.message = QLabel()
        self.message.setObjectName("alertMessage")
        self.message.setWordWrap(True)

        layout.addWidget(self.message, 1)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

        self.hide()

    def show_message(self, message, success=False):
        self.timer.stop()

        status = "success" if success else "error"

        self.setProperty("status", status)
        self.message.setProperty("status", status)
        self.message.setText(message)

        for widget in (self, self.message):
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()

        self.show()
        self.timer.start(4000)

    def dismiss(self):
        self.timer.stop()
        self.hide()
