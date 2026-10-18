
from ui.PySide6_Qt import *
from config.config_loader import load_config
from utils.paths import resource_path

IMAGES = load_config("device_images.json")

class DeviceModelRow(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent)

        self.setObjectName("deviceModelRow")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(12)

        image = QLabel()
        image.setObjectName("modelRowImage")
        image.setFixedSize(52, 52)
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_path = IMAGES.get(model["model"])

        if image_path:
            pixmap = QPixmap(str(resource_path(image_path)))
            image.setPixmap(
                pixmap.scaled(
                    60, 60,
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

        version = QLabel(f"HW v{model['hardware_version']}")
        version.setObjectName("modelHardwareVersion")

        texts.addWidget(code)
        texts.addWidget(name)
        texts.addWidget(version)

        ports = QLabel(f"{model['port_count']} Port(s)")
        ports.setObjectName("modelPorts")

        arrow = QLabel("›")
        arrow.setObjectName("modelArrow")

        layout.addWidget(image)
        layout.addLayout(texts, 1)
        layout.addWidget(ports)
        layout.addWidget(arrow)
