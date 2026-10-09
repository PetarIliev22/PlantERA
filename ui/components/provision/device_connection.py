import qtawesome as qta
from enum import Enum
from ui.PySide6_Qt import *
from serial.tools import list_ports
from ui.dialogs.boot_dialog import BootDialog
from config.config_loader import load_config

texts = load_config("device_connection.json")

class ConnectionState(Enum):
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"

class DeviceConnection(QFrame):
    connected = Signal(str, dict)
    disconnected = Signal()

    def __init__(self, parent):
        super().__init__(parent)

        self.state = ConnectionState.DISCONNECTED
        self.connected_port = None
        
        self.setObjectName("connectionCard")
        self.setFixedHeight(170)

        self.create_ui()
        self.refresh_ports()
        self.set_state(ConnectionState.DISCONNECTED)

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 16, 14, 14)
        layout.setSpacing(0)

        self.create_title(layout)
        self.create_port_row(layout)
        self.create_status_row(layout)

        layout.addStretch()

    def create_title(self, layout):
        row = QHBoxLayout()
        row.setContentsMargins(10, 0, 0, 0)
        row.setSpacing(10)

        icon = QLabel()
        icon.setPixmap(
            qta.icon(
                "fa6s.link",
                color="#1687F8"
            ).pixmap(23, 23)
        )

        title = QLabel("Device Connection")
        title.setObjectName("connectionTitle")

        row.addWidget(icon)
        row.addWidget(title)
        row.addStretch()

        layout.addLayout(row)

    def create_port_row(self, layout):
        row = QHBoxLayout()
        row.setContentsMargins(0, 16, 0, 0)
        row.setSpacing(0)

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

        self.connect_button = QPushButton()
        self.connect_button.setObjectName("connectButton")
        self.connect_button.setFixedSize(115, 35)
        self.connect_button.clicked.connect(self.toggle_connection)

        row.addWidget(label)
        row.addWidget(self.com_box, 1)
        row.addSpacing(10)
        row.addWidget(self.refresh_button)
        row.addSpacing(15)
        row.addWidget(self.connect_button)

        layout.addLayout(row)

    def create_status_row(self, layout):
        row = QHBoxLayout()
        row.setContentsMargins(0, 12, 0, 0)
        row.setSpacing(5)

        self.status_dot = QLabel("●")
        self.status_dot.setObjectName("statusDot")
        self.status_dot.setFixedWidth(20)
        
        label = QLabel("Status:")
        label.setObjectName("connectionLabel")
        label.setFixedWidth(80)


        self.status_text = QLabel()
        self.status_text.setObjectName("statusText")

        row.addWidget(label)
        row.addWidget(self.status_dot)
        row.addWidget(self.status_text)
        row.addStretch()

        layout.addLayout(row)

    def refresh_ports(self):
        self.com_box.clear()
        ports = list_ports.comports()

        for port in ports:
            self.com_box.addItem(
                f"{port.device} - {port.description}",
                port.device
            )

        if not ports:
            self.com_box.addItem(
                "No devices found",
                None
            )

    def toggle_connection(self):
        if self.state is ConnectionState.CONNECTED:
            self.disconnect_device()
        else:
            self.connect_device()

    def connect_device(self):
        port = self.com_box.currentData()

        if not port:
            return

        self.boot_dialog = BootDialog(
            self.window(),
            port,
            lambda info: self.device_connected(port, info)
        )

    def disconnect_device(self):
        self.connected_port = None
        self.set_state(ConnectionState.DISCONNECTED)
        self.disconnected.emit()

    def device_connected(self, port, info):
        print(self.connected_port)
        self.set_state(ConnectionState.CONNECTED)
        self.connected.emit(port, info)

    def set_state(self, state):
        self.state = state
    
        self.status_text.setText(
            texts["status"][state.value]
        )

        self.connect_button.setText(
            texts["button"][state.value]
        )

        for widget in (self.status_dot, self.status_text):
            widget.setProperty(
                "status",
                state.value
            )

            widget.style().unpolish(widget)
            widget.style().polish(widget)