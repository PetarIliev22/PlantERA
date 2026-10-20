
from ui.PySide6_Qt import *
from config.version import APP_VERSION
from config.config_loader import load_config
from ui.updater_window import launch_updater

texts = load_config("update_dialog.json")

class UpdateDialog(QFrame):
    def __init__(self, parent, update):
        super().__init__(parent)

        self.update = update

        self.setObjectName("updateOverlay")
        self.setGeometry(parent.rect())

        self.card = QFrame(self)
        self.card.setObjectName("updateDialog")
        self.card.setFixedWidth(520)

        overlay_layout = QVBoxLayout(self)
        overlay_layout.addWidget(self.card,alignment=Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Title
        self.title = QLabel(texts["title"].format(version=update["version"]))
        self.title.setObjectName("updateTitle")

        # Description
        self.description = QLabel(texts["description"].format(current_version=APP_VERSION))
        self.description.setObjectName("updateDescription")

        # Update button
        self.update_button = QPushButton(texts["buttons"]["update"])
        self.update_button.setObjectName("updateButton")
        self.update_button.clicked.connect(self.start_update)

        # Later button
        self.later_button = QPushButton(texts["buttons"]["later"])
        self.later_button.setObjectName("laterButton")
        self.later_button.clicked.connect(self.close)

        # Button Layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.addWidget(self.update_button)
        buttons_layout.addWidget(self.later_button)
        
        layout.addWidget(self.title)
        layout.addWidget(self.description)
        layout.addSpacing(10)
        layout.addLayout(buttons_layout)

    def start_update(self):
        launch_updater(self.update)

def show_update_dialog(parent, update):
    dialog = UpdateDialog(parent, update)
    dialog.raise_()
    dialog.show()

    return dialog
