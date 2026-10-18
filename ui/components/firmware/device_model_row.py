
from ui.PySide6_Qt import *
from utils.paths import resource_path
from config.config_loader import load_config

images = load_config("device_images.json")

class DeviceModelRow(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)

        self.setObjectName("deviceModelRow")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 6, 14, 6)
        layout.setSpacing(12)
        
        image = QLabel()
        image.setObjectName("modelRowImage")
        image.setFixedSize(52, 52)
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        image_path = images.get(model["model"])
        if image_path:
            pixmap = QPixmap(str(resource_path(image_path)))

            image.setPixmap(
                pixmap.scaled(
                    44, 44,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
        
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

        layout.addWidget(image)
        layout.addLayout(texts, 1)
        layout.addWidget(ports)
        layout.addWidget(arrow)
