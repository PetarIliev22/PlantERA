from ui.PySide6_Qt import *

class FirmwareView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("firmwareView")