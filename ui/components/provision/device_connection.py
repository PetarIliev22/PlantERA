import qtawesome as qta

from ui.PySide6_Qt import *
from serial.tools import list_ports
from ui.dialogs.boot_dialog import BootDialog


class DeviceConnection(QFrame):
    connected = Signal(str)
    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName("connectionCard")
        self.setFixedHeight(170)

        self.create_ui()
        self.refresh_ports()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 16, 14, 14)
        layout.setSpacing(0)

        self.create_title(layout)
        self.create_com_row(layout)
        self.create_status_row(layout)

        layout.addStretch()

    def create_title(self, layout):
        row = QFrame()
        row.setObjectName("titleRow")

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(10, 0, 0, 0)
        row_layout.setSpacing(10)

        icon = QLabel()
        icon.setPixmap(
            qta.icon(
                "fa6s.link",
                color="#1687F8"
            ).pixmap(23, 23)
        )

        title = QLabel("Device Connection")
        title.setObjectName("connectionTitle")

        row_layout.addWidget(icon)
        row_layout.addWidget(title)
        row_layout.addStretch()

        layout.addWidget(row)

    def create_com_row(self, layout):
        row = QFrame()
        row.setObjectName("comRow")

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 16, 0, 0)
        row_layout.setSpacing(0)

        label = QLabel("COM Port:")
        label.setObjectName("connectionLabel")
        label.setFixedWidth(80)

        self.com_box = QComboBox()
        self.com_box.setObjectName("comBox")
        self.com_box.setFixedHeight(35)

        self.refresh_button = QPushButton()
        self.refresh_button.setObjectName("refreshButton")
        self.refresh_button.setFixedSize(40, 35)
        self.refresh_button.setIcon(
            qta.icon(
                "fa6s.arrows-rotate",
                color="#1687F8"
            )
        )
        self.refresh_button.clicked.connect(self.refresh_ports)

        self.connect_button = QPushButton("Connect")
        self.connect_button.setObjectName("connectButton")
        self.connect_button.setFixedSize(115, 35)
        self.connect_button.clicked.connect(self.connect_device)

        row_layout.addWidget(label)
        row_layout.addWidget(self.com_box, 1)
        row_layout.addSpacing(10)
        row_layout.addWidget(self.refresh_button)
        row_layout.addSpacing(15)
        row_layout.addWidget(self.connect_button)

        layout.addWidget(row)

    def create_status_row(self, layout):
        row = QFrame()
        row.setObjectName("statusRow")

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 12, 0, 0)
        row_layout.setSpacing(5)

        label = QLabel("Status:")
        label.setObjectName("connectionLabel")
        label.setFixedWidth(80)

        self.status_dot = QLabel("●")
        self.status_dot.setObjectName("statusDot")
        self.status_dot.setFixedWidth(20)

        self.status_text = QLabel("Disconnected")
        self.status_text.setObjectName("statusText")

        self.set_status(
            "Disconnected",
            "disconnected"
        )

        row_layout.addWidget(label)
        row_layout.addWidget(self.status_dot)
        row_layout.addWidget(self.status_text)
        row_layout.addStretch()

        layout.addWidget(row)

    def refresh_ports(self):
        ports = [
            f"{port.device} - {port.description}"
            for port in list_ports.comports()
        ]

        self.com_box.clear()

        if ports:
            self.com_box.addItems(ports)
            self.com_box.setCurrentIndex(0)
        else:
            self.com_box.addItem("No devices found")

    def set_status(self, text, status):
        self.status_text.setText(text)

        for widget in (
            self.status_dot,
            self.status_text
        ):
            widget.setProperty("status", status)
            widget.style().unpolish(widget)
            widget.style().polish(widget)

    def connect_device(self):
        if self.connect_button.text() == "Disconnect":
            self.set_status(
                "Disconnected",
                "disconnected"
            )

            self.connect_button.setText("Connect")
            return

        selected = self.com_box.currentText()

        if selected in (
            "",
            "No devices found",
            "No device selected"
        ):
            return

        port = selected.split(" - ")[0]

        self.boot_dialog = BootDialog(
            self.window(),
            port,
            self.device_connected
        )

    def device_connected(self):
        self.set_status(
            "Connected",
            "connected"
        )

        self.connect_button.setText(
            "Disconnect"
        )
        
        self.connected.emit(
            self.com_box.currentText().split(" - ")[0]
        )