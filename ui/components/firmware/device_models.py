
from ui.common.PySide6_Qt import *
from utils.svg_icons import svg_icon
from ui.components.firmware.device_model_row import DeviceModelRow
from ui.components.loading_spinner import LoadingSpinner

class DeviceModels(QFrame):
    model_selected = Signal(dict)
    retry_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("deviceModelsCard")
        self.models = []

        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 18)
        layout.setSpacing(12)

        # Header
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

        # Models list
        self.models_list = QListWidget()
        self.models_list.setObjectName("deviceModelsList")
        self.models_list.setSpacing(5)
        self.models_list.currentItemChanged.connect(
            self.on_model_selected
        )

        # Empty state
        self.empty_state = QWidget()
        empty_layout = QVBoxLayout(self.empty_state)
        empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        empty_icon = QLabel()
        empty_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_icon.setPixmap(
            svg_icon("no_models.svg", "#A0AEC0", 72).pixmap(72, 72)
        )

        empty_layout.addWidget(empty_icon)

        # Loading state
        self.loading_state = QWidget()
        loading_layout = QVBoxLayout(self.loading_state)
        loading_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        loading_layout.setSpacing(12)

        self.spinner = LoadingSpinner()

        loading_title = QLabel("Loading models...")
        loading_title.setObjectName("modelsLoadingText")

        loading_subtitle = QLabel("Fetching registered device models.")
        loading_subtitle.setObjectName("modelsLoadingSubtitle")
        
        for label in (loading_title, loading_subtitle):
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        loading_layout.addWidget(
            self.spinner,
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        loading_layout.addWidget(loading_title)
        loading_layout.addWidget(loading_subtitle)

        # Error state
        self.error_state = QWidget()
        error_layout = QVBoxLayout(self.error_state)
        error_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_layout.setSpacing(12)

        error_title = QLabel("Failed to load models")
        error_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        error_description = QLabel("Check your connection and try again.")
        error_description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.retry_button = QPushButton("Try Again")
        self.retry_button.setObjectName("retryModelsButton")
        self.retry_button.setFixedSize(130, 36)
        self.retry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.retry_button.clicked.connect(self.retry_requested.emit)

        error_layout.addWidget(error_title)
        error_layout.addWidget(error_description)
        error_layout.addWidget(
            self.retry_button,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Content stack
        self.content_stack = QStackedWidget()

        for widget in (
            self.loading_state,
            self.empty_state,
            self.models_list,
            self.error_state
        ):
            self.content_stack.addWidget(widget)

        layout.addWidget(self.content_stack)

    def set_loading(self):
        self.content_stack.setCurrentWidget(self.loading_state)
        self.spinner.start()

    def set_models(self, models):
        self.spinner.stop()
        self.models = models
        self.models_list.clear()

        for model in models:
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, model)
            item.setSizeHint(QSize(0, 65))

            self.models_list.addItem(item)
            self.models_list.setItemWidget(
                item,
                DeviceModelRow(model, self.models_list)
            )

        self.content_stack.setCurrentWidget(
            self.models_list if models else self.empty_state
        )
        
        if models:
            self.models_list.setCurrentRow(0)

    def on_model_selected(self, current):
        if current is None:
            return

        model = current.data(
            Qt.ItemDataRole.UserRole
        )

        self.model_selected.emit(model)
    
    def set_error(self):
        self.spinner.stop()
        self.content_stack.setCurrentWidget(self.error_state)
