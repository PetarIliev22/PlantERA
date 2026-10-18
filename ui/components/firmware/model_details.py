
from ui.PySide6_Qt import *
from utils.svg_icons import svg_icon
from utils.paths import resource_path
from config.config_loader import load_config

IMAGES = load_config("device_images.json")

class ModelDetails(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("modelDetailsCard")
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(0)

        # Header
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

        # Main content
        content = QHBoxLayout()
        content.setSpacing(12)

        # Left: device image
        self.image = QLabel()
        self.image.setObjectName("modelDetailsImage")
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image.setMinimumWidth(150)
        self.image.setFixedHeight(190)
        self.image.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed
        )

        content.addWidget(self.image, 0, Qt.AlignmentFlag.AlignTop)

        # Right: device information
        info = QVBoxLayout()
        info.setSpacing(4)

        self.name = QLabel()
        self.name.setObjectName("modelDetailsName")
        self.name.setWordWrap(True)

        self.code = QLabel()
        self.code.setObjectName("modelDetailsCode")

        self.hardware_version = QLabel()
        self.hardware_version.setObjectName("modelDetailsMeta")

        self.port_count = QLabel()
        self.port_count.setObjectName("modelDetailsMeta")

        self.ports = QLabel()
        self.ports.setObjectName("modelDetailsMeta")
        self.ports.setWordWrap(True)

        for widget in (
            self.name,
            self.code,
            self.hardware_version,
            self.port_count,
            self.ports
        ):
            info.addWidget(widget)

        # Technical specifications
        specifications_title = QLabel("Technical Specifications")
        specifications_title.setObjectName("modelDetailsSectionTitle")
        info.addWidget(specifications_title)

        self.specifications_layout = QGridLayout()
        self.specifications_layout.setSpacing(4)
        info.addLayout(self.specifications_layout)

        # Description
        description_title = QLabel("Description")
        description_title.setObjectName("modelDetailsSectionTitle")

        self.description = QLabel()
        self.description.setObjectName("modelDetailsDescription")
        self.description.setWordWrap(True)

        info.addWidget(description_title)
        info.addWidget(self.description)
        info.addStretch()

        content.addLayout(info, 1)

        self.details_widget = QWidget()
        self.details_widget.setObjectName("modelDetailsContent")
        self.details_widget.setLayout(content)

        self.content_stack = QStackedWidget()

        self.skeleton = self.create_skeleton()

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("modelDetailsScroll")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.scroll_area.setWidget(self.details_widget)

        self.content_stack.addWidget(self.skeleton)
        self.content_stack.addWidget(self.scroll_area)

        layout.addWidget(self.content_stack, 1)

    def set_model(self, model):
        self.name.setText(model.get("name") or "")
        self.code.setText(model["model"])

        self.hardware_version.setText(
            f"Hardware Version: {model.get('hardware_version') or 'N/A'}"
        )

        self.port_count.setText(
            f"Sensor Ports: {model.get('port_count', 0)}"
        )

        ports = model.get("ports") or {}
        self.ports.setText(
            "Port Mapping: " + ", ".join(
                f"{port} → GPIO{data['gpio']}"
                for port, data in ports.items()
            )
        )

        self.description.setText(model.get("description") or "")

        # Device image
        self.image.clear()
        image_path = IMAGES.get(model["model"])

        if image_path:
            pixmap = QPixmap(str(resource_path(image_path)))
            self.image.setPixmap(
                pixmap.scaled(
                    180, 180,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

        # Clear previous specifications
        while self.specifications_layout.count():
            item = self.specifications_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        # Specifications from Supabase
        specifications = model.get("specifications") or {}

        for index, (key, value) in enumerate(specifications.items()):
            label = key.replace("_", " ").title()

            if isinstance(value, list):
                value = ", ".join(map(str, value))

            field = QLabel(f"{label}\n{value}")
            field.setObjectName("modelSpecification")
            field.setWordWrap(True)

            self.specifications_layout.addWidget(
                field,
                index // 2,
                index % 2
            )
            
        self.content_stack.setCurrentWidget(self.scroll_area)
            
    def create_skeleton(self):
        skeleton = QWidget()

        layout = QHBoxLayout(skeleton)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        image = QFrame()
        image.setObjectName("skeletonImage")
        image.setMinimumWidth(150)

        info = QVBoxLayout()
        info.setSpacing(10)

        for width in (220, 90, 160, 140):
            line = QFrame()
            line.setObjectName("skeletonLine")
            line.setFixedSize(width, 13)
            info.addWidget(line)

        info.addSpacing(8)

        specs = QGridLayout()
        specs.setSpacing(8)

        for index in range(4):
            block = QFrame()
            block.setObjectName("skeletonSpec")
            block.setFixedHeight(45)

            specs.addWidget(block, index // 2, index % 2)

        info.addLayout(specs)
        info.addSpacing(8)

        description = QFrame()
        description.setObjectName("skeletonDescription")
        description.setFixedHeight(42)

        info.addWidget(description)
        info.addStretch()

        layout.addWidget(image, 1)
        layout.addLayout(info, 2)

        return skeleton
