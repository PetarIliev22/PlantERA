import qtawesome as qta

from ui.PySide6_Qt import *


DEFAULT_VALUE = "-- / --"


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

        self.board_value = self.create_row(layout, "Board:")
        self.uid_value = self.create_row(layout, "Chip ID (UID):", copy=True)
        self.firmware_value = self.create_row(layout, "Firmware:")
        self.signature_value = self.create_row(layout, "Signature:")

        layout.addStretch()

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

            row.addWidget(button)

        row.addStretch()
        layout.addLayout(row)

        return value

    def set_device_info(
        self,
        board=DEFAULT_VALUE,
        uid=DEFAULT_VALUE,
        firmware=DEFAULT_VALUE,
        signature=DEFAULT_VALUE
    ):
        self.board_value.setText(board)
        self.uid_value.setText(uid)
        self.firmware_value.setText(firmware)
        self.signature_value.setText(signature)
        
    def clear(self):
        self.set_device_info()