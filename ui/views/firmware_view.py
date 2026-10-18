
from ui.PySide6_Qt import *
from ui.components.firmware.device_models import DeviceModels
from ui.components.firmware.model_details import ModelDetails
from utils.shadow import apply_shadow

class FirmwareView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("firmwareView")
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Top components
        self.device_models = DeviceModels(self)
        self.model_details = ModelDetails(self)

        apply_shadow(self.device_models)
        apply_shadow(self.model_details)

        self.top_layout = QHBoxLayout()
        self.top_layout.setSpacing(20)

        self.top_layout.addWidget(self.device_models, 1)
        self.top_layout.addWidget(self.model_details, 1)

        layout.addLayout(self.top_layout, 1)

        # Bottom components
        self.bottom_container = QWidget(self)
        self.bottom_container.setObjectName("firmwareBottomContainer")

        layout.addWidget(self.bottom_container, 1)

        # Model selection
        self.device_models.model_selected.connect(
            self.model_details.set_model
        )
