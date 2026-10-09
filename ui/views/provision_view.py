from ui.PySide6_Qt import *

from ui.components.provision.device_connection import DeviceConnection
from ui.components.provision.device_info import DeviceInfo

class ProvisionView(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName("provisionView")
        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        self.device_connection = DeviceConnection(self)
        self.device_info = DeviceInfo(self)


        self.device_connection.connected.connect(
            self.device_connected
        )

        self.device_connection.disconnected.connect(
            self.device_disconnected
        )

        connection_row = QHBoxLayout()
        connection_row.addWidget(self.device_connection, 65)
        connection_row.addStretch(35)

        info_row = QHBoxLayout()
        info_row.addWidget(self.device_info, 65)
        info_row.addStretch(35)

        layout.addLayout(connection_row)
        layout.addLayout(info_row)
        layout.addStretch()

    def device_connected(self, port, info):
        self.device_info.set_device_info(
            board=info["board"],
            uid=info["uid"]
        )
        
    def device_disconnected(self):
        self.device_info.clear()