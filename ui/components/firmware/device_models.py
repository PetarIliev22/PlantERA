
from ui.PySide6_Qt import *
from utils.svg_icons import svg_icon

class DeviceModels(QFrame):
    model_selected = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("deviceModelsCard")
        self.models = []

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
            svg_icon("microchip.svg", "#1687F8", 23).pixmap(23, 23)
        )

        title = QLabel("Registered Models")
        title.setObjectName("deviceModelsTitle")

        self.add_button = QPushButton("+ Add Model")
        self.add_button.setObjectName("addModelButton")
        self.add_button.setFixedHeight(35)
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)

        header.addWidget(icon)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.add_button)

        layout.addLayout(header)


        self.models_list = QListWidget()
        self.models_list.setObjectName("deviceModelsList")
        self.models_list.setSpacing(5)

        self.models_list.currentItemChanged.connect(
            self.on_model_selected
        )

        layout.addWidget(self.models_list)

    def set_models(self, models):
        self.models = models
        self.models_list.clear()

        for model in models:
            item = QListWidgetItem(
                model.get("name") or model["model"]
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                model
            )

            self.models_list.addItem(item)

        if models:
            self.models_list.setCurrentRow(0)

    def on_model_selected(self, current, previous):
        if current is None:
            return

        model = current.data(
            Qt.ItemDataRole.UserRole
        )

        self.model_selected.emit(model)
