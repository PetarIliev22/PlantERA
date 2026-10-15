from ui.PySide6_Qt import *
from utils.svg_icons import svg_icon
from config.config_loader import load_config

actions = load_config("device_actions.json")["actions"]

class DeviceActions(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setObjectName("deviceActionsCard")
        self.setFixedHeight(110)

        self.create_ui()
        
    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(10)

        self.create_title(layout)
        self.create_buttons(layout)
    
    def create_title(self, layout):
        row = QHBoxLayout()
        row.setSpacing(10)

        icon = QLabel()
        icon.setPixmap(
            svg_icon("bolt.svg", "#1687F8", 20).pixmap(20, 20)
        )

        title = QLabel("Actions")
        title.setObjectName("deviceActionsTitle")

        row.addWidget(icon)
        row.addWidget(title)
        row.addStretch()

        layout.addLayout(row)
        
    def create_buttons(self, layout):
        row = QHBoxLayout()
        row.setSpacing(10)

        for action in actions:
            name = action["id"]
            color = action["color"]

            button = QPushButton()
            button.setObjectName(f"{name}Button")
            button.setMinimumHeight(58)
            button.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed
            )

            button_layout = QHBoxLayout(button)
            button_layout.setContentsMargins(12, 6, 8, 6)
            button_layout.setSpacing(12)

            icon_label = QLabel()
            icon_label.setPixmap(
                svg_icon(
                    action["icon"],
                    color,
                    35
                ).pixmap(35, 35)
            )
            icon_label.setAttribute(
                Qt.WidgetAttribute.WA_TransparentForMouseEvents
            )

            text_layout = QVBoxLayout()
            text_layout.setSpacing(3)

            title_label = QLabel(action["title"])
            title_label.setObjectName(f"{name}ButtonTitle")

            subtitle_label = QLabel(action["subtitle"])
            subtitle_label.setObjectName("actionSubtitle")

            for widget in (title_label, subtitle_label):
                widget.setAttribute(
                    Qt.WidgetAttribute.WA_TransparentForMouseEvents
                )

            text_layout.addWidget(title_label)
            text_layout.addWidget(subtitle_label)

            button_layout.addWidget(icon_label)
            button_layout.addLayout(text_layout, 1)

            row.addWidget(button, 1)

            setattr(self, f"{name}_button", button)

        layout.addLayout(row)