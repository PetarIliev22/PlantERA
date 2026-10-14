from ui.PySide6_Qt import *

class SettingsView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("settingsView")