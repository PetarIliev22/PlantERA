
from ui.PySide6_Qt import *
from utils.svg_icons import svg_icon
from utils.paths import resource_path

class ModelDetails(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("modelDetailsCard")
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 18)
        layout.setSpacing(12)

        header = QHBoxLayout()
        header.setContentsMargins(10, 0, 0, 0)
        header.setSpacing(10)

        icon = QLabel()
        icon.setPixmap(
            svg_icon("circle-info.svg", "#1687F8", 23).pixmap(23, 23)
        )

        title = QLabel("Model Details")
        title.setObjectName("modelDetailsTitle")

        header.addWidget(icon)
        header.addWidget(title)
        header.addStretch()

        layout.addLayout(header)

        self.image = QLabel()
        self.image.setObjectName("modelDetailsImage")
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setMinimumHeight(120)

        layout.addWidget(self.image, 1)

        self.description = QLabel()
        self.description.setObjectName("modelDetailsDescription")
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hardware_version = QLabel()
        self.hardware_version.setObjectName("modelDetailsInfo")

        self.port_count = QLabel()
        self.port_count.setObjectName("modelDetailsInfo")

        layout.addWidget(self.description)
        layout.addWidget(self.hardware_version)
        layout.addWidget(self.port_count)

    def set_model(self, model):
        self.description.setText(
            model.get("description") or ""
        )

        self.hardware_version.setText(
            f"Hardware Version: {model.get('hardware_version') or 'N/A'}"
        )

        self.port_count.setText(
            f"Sensor Ports: {model.get('port_count', 0)}"
        )
