import qtawesome as qta
from enum import Enum
from ui.PySide6_Qt import *
from serial.tools import list_ports
from config.config_loader import load_config

texts = load_config("device_connection.json")

class ConnectionState(Enum):
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    FAILED = "failed"

class DeviceConnection(QFrame):
    connected = Signal(str, dict)
    disconnected = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.state = ConnectionState.DISCONNECTED
        self.connected_port = None
        
        self.setObjectName("connectionCard")
        self.setFixedHeight(140)

        self.create_ui()
        self.refresh_ports()
        self.port_timer = QTimer(self)
        self.port_timer.timeout.connect(self.refresh_ports)
        self.port_timer.start(500)
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
        label.setWordWrap(True)
        label.setFixedWidth(70)


        self.status_text = QLabel()
        self.status_text.setObjectName("statusText")

        row.addWidget(label)
        row.addWidget(self.status_dot)
        row.addWidget(self.status_text)
        row.addStretch()

        layout.addLayout(row)

    def refresh_ports(self):
        current_port = self.com_box.currentData()
        
        ports = list_ports.comports()
        port_names = [port.device for port in ports]

        if (
            self.state is ConnectionState.CONNECTED
            and self.connected_port not in port_names
        ):
            self.disconnect_device()
            return

        if self.state is ConnectionState.CONNECTED:
            return

        self.com_box.clear()

        for port in ports:
            self.com_box.addItem(
                f"{port.device} - {port.description}",
                port.device
            )

        if not ports:
            self.com_box.addItem("No devices found", None)
            
        index = self.com_box.findData(current_port)

        if index >= 0:
            self.com_box.setCurrentIndex(index)

    def toggle_connection(self):
        if self.state is ConnectionState.CONNECTED:
            self.disconnect_device()
        else:
            self.connect_device()

    def connect_device(self):
        from ui.dialogs.boot_dialog import BootDialog
       
        port = self.com_box.currentData()
        if not port:
            self.set_state(ConnectionState.FAILED)
        
            QTimer.singleShot(
                3000,
                lambda: (
                    self.set_state(ConnectionState.DISCONNECTED)
                    if self.state is ConnectionState.FAILED
                    else None
                )
            )
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
        self.connected_port = port
        self.set_state(ConnectionState.CONNECTED)
        self.connected.emit(port, info)
        
    def set_state(self, state):
        self.state = state
        connected = state == ConnectionState.CONNECTED
    
        self.com_box.setEnabled(not connected)
        self.refresh_button.setEnabled(not connected)
        
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