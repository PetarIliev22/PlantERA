import qtawesome as qta

from ui.PySide6_Qt import *


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
        self.uid_value = self.create_uid_row(layout)
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

    def create_row(self, layout, label_text):
        row = QHBoxLayout()
        row.setSpacing(15)

        label = QLabel(label_text)
        label.setObjectName("deviceInfoLabel")
        label.setFixedWidth(115)

        value = QLabel("No Information Available")
        value.setObjectName("deviceInfoValue")

        row.addWidget(label)
        row.addWidget(value)
        row.addStretch()

        layout.addLayout(row)

        return value

    def create_uid_row(self, layout):
        row = QHBoxLayout()
        row.setSpacing(15)

        label = QLabel("Chip ID (UID):")
        label.setObjectName("deviceInfoLabel")
        label.setFixedWidth(115)

        value = QLabel("--/--")
        value.setObjectName("deviceInfoValue")

        copy_button = QPushButton()
        copy_button.setObjectName("copyButton")
        copy_button.setFixedSize(38, 38)
        copy_button.setIcon(
            qta.icon(
                "fa6s.copy",
                color="#8491A5"
            )
        )

        row.addWidget(label)
        row.addWidget(value)
        row.addWidget(copy_button)
        row.addStretch()

        layout.addLayout(row)

        return value

    def set_device_info(
        self,
        board="--/--",
        uid="--/--",
        firmware="--/--",
        signature="--/--"
    ):
        self.board_value.setText(board)
        self.uid_value.setText(uid)
        self.firmware_value.setText(firmware)
        self.signature_value.setText(signature)