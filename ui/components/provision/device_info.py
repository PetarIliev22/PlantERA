import qtawesome as qta

from ui.PySide6_Qt import *

DEFAULT_VALUE = "Not available"

rows = [
    ("board", "Board:", False),
    ("uid", "Chip ID (UID):", True),
    ("firmware", "Firmware:", False),
    ("signature", "Signature:", False),
]

class DeviceInfo(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName("deviceInfoCard")
        self.setFixedHeight(200)

        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        self.create_title(layout)
        
        for name, text, copy in rows:
            setattr(self, name, self.create_row(layout, text, copy))
        
    def create_title(self, layout):
        row = QHBoxLayout()
        row.setSpacing(12)

        icon = QLabel()
        icon.setPixmap(
            qta.icon(
                "fa6s.microchip",
                color="#1687F8"
            ).pixmap(26, 26)
        )

        title = QLabel("Device Information")
        title.setObjectName("deviceInfoTitle")

        row.addWidget(icon)
        row.addWidget(title)
        row.addStretch()

        layout.addLayout(row)
        layout.addSpacing(6)

    def create_row(self, layout, label_text, copy=False):
        row = QHBoxLayout()
        row.setSpacing(15)

        label = QLabel(label_text)
        label.setObjectName("deviceInfoLabel")
        label.setFixedWidth(115)

        value = QLabel(DEFAULT_VALUE)
        value.setObjectName("deviceInfoValue")

        row.addWidget(label)
        row.addWidget(value)

        if copy:
            button = QPushButton()
            button.setObjectName("copyButton")
            button.setFixedSize(38, 38)
            button.setIcon(
                qta.icon(
                    "fa6s.copy",
                    color="#8491A5"
                )
            )
            
            button.clicked.connect(
                lambda: QApplication.clipboard().setText(value.text())
            )
            
            row.addWidget(button)

        row.addStretch()
        layout.addLayout(row)

        return value
    
    def set_device_info(self, **info):
        for name, *_ in rows:
            getattr(self, name).setText(
                info.get(name) or DEFAULT_VALUE
            )
        
    def clear(self):
        self.set_device_info()