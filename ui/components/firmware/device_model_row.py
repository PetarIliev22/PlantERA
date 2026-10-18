
from ui.PySide6_Qt import *

class DeviceModelRow(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)

        self.setObjectName("deviceModelRow")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 6, 14, 6)
        layout.setSpacing(12)

        texts = QVBoxLayout()
        texts.setSpacing(3)

        code = QLabel(model["model"])
        code.setObjectName("modelCode")

        name = QLabel(model["name"])
        name.setObjectName("modelName")

        texts.addWidget(code)
        texts.addWidget(name)

        ports = QLabel(f"{model['port_count']} Ports")
        ports.setObjectName("modelPorts")

        arrow = QLabel("›")
        arrow.setObjectName("modelArrow")

        layout.addLayout(texts, 1)
        layout.addWidget(ports)
        layout.addWidget(arrow)
