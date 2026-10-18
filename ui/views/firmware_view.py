import asyncio
from importlib import import_module
from ui.PySide6_Qt import *
from ui.components.firmware.device_models import DeviceModels
from ui.components.firmware.model_details import ModelDetails
from utils.shadow import apply_shadow

class FirmwareView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("firmwareView")
        self.create_ui()
        
        asyncio.get_running_loop().create_task(self.load_models())
        
    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Top components
        self.device_models = DeviceModels(self)
        self.model_details = ModelDetails(self)

        for widget in(
            self.device_models,
            self.model_details
        ):
            apply_shadow(widget)

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
        
    async def load_models(self):
        self.device_models.set_loading()
        try:
            module = await asyncio.to_thread(
                import_module,
                "services.supabase_service"
            )

            models = await module.supabase_service.get_device_models()
            self.device_models.set_models(models)

        except Exception as error:
            print(f"Supabase Error: {error}")


