import qtawesome as qta

from ui.PySide6_Qt import *

class DeviceConsole(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        set.objectName("deviceConsoleCard")
        set.setFixedHeight(300)