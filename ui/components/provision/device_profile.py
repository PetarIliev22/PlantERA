import qtawesome as qta

from ui.PySide6_Qt import *
from config.config_loader import load_config
from utils.paths import resource_path

profiles = load_config("device_profiles.json")["profiles"]

class DeviceProfile(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName("deviceProfileCard")
        self.setMinimumHeight(390)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        
        self.create_ui()
        self.show_empty()

    def create_ui(self):
        self.stack = QStackedLayout(self)

        self.empty_page = self.create_empty_page()
        self.profile_page = self.create_profile_page()

        self.stack.addWidget(self.empty_page)
        self.stack.addWidget(self.profile_page)

    def create_empty_page(self):
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        icon = QLabel()
        icon.setPixmap(
            qta.icon(
                "fa6s.microchip",
                color="#AAB4C3"
            ).pixmap(48, 48)
        )
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        text = QLabel("No device detected")
        text.setObjectName("deviceProfileEmptyText")
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(icon)
        layout.addWidget(text)

        return page

    def create_profile_page(self):
        page = QWidget()

        self.profile_layout = QBoxLayout(
            QBoxLayout.Direction.LeftToRight,
            page
        )

        layout = self.profile_layout
        layout.setContentsMargins(14, 18, 14, 18)
        layout.setSpacing(12)

        self.image = QLabel()
        self.image.setObjectName("deviceProfileImage")
        self.image.setMinimumWidth(120)
        self.image.setMaximumWidth(170)
        self.image.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
    
        right = QVBoxLayout()
        right.setSpacing(10)

        self.title = QLabel()
        self.title.setObjectName("deviceProfileTitle")
        self.title.setWordWrap(True)
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.specs_layout = QVBoxLayout()
        self.specs_layout.setSpacing(6)

        right.addWidget(self.title)
        right.addSpacing(10)
        right.addLayout(self.specs_layout)
        right.addStretch()

        layout.addWidget(self.image, 1)
        layout.addLayout(right, 1)

        return page
    
    @staticmethod
    def find_profile(chip):
        return next(
            (
                profile
                for profile in profiles
                if any(
                    supported_chip in chip
                    for supported_chip in profile["chip"]
                )
            ),
            None
        )
        
    def load_profile(self, chip):
        self.clear_specs()
        profile = self.find_profile(chip)

        if not profile:
            self.show_empty()
            return

        self.title.setText(profile["name"])
        
        pixmap = QPixmap(str(resource_path(*profile["image"].split("/"))))
        self.image.setPixmap(
            pixmap.scaled(
                180,
                320,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
        
        for spec in profile["specs"]:
            self.add_spec(spec["label"], spec["value"])
            
        self.show_profile()
    
    def add_spec(self, label_text, value_text):
        row = QHBoxLayout()
        row.setSpacing(8)

        label = QLabel(label_text)
        label.setObjectName("deviceProfileSpecLabel")
        label.setFixedWidth(75)

        value = QLabel(value_text)
        value.setObjectName("deviceProfileSpecValue")
        value.setWordWrap(True)

        row.addWidget(label)
        row.addWidget(value, 1)

        self.specs_layout.addLayout(row)
    
    def clear_specs(self):
        while self.specs_layout.count():
            item = self.specs_layout.takeAt(0)

            if item.layout():
                while item.layout().count():
                    child = item.layout().takeAt(0)

                    if child.widget():
                        child.widget().deleteLater()    

    def show_empty(self):
        self.stack.setCurrentWidget(self.empty_page)

    def show_profile(self):
        self.stack.setCurrentWidget(self.profile_page)