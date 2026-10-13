from ui.PySide6_Qt import *

from ui.components.provision.device_connection import DeviceConnection
from ui.components.provision.device_info import DeviceInfo
from ui.components.provision.device_profile import DeviceProfile

class ProvisionView(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName("provisionView")
        self.create_ui()
        self.fade_in()

    def fade_in(self):
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.fade_animation = QPropertyAnimation(
            self.opacity_effect,
            b"opacity"
        )

        self.fade_animation.setDuration(200)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)

        self.fade_animation.start()
    
    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        self.device_connection = DeviceConnection(self)
        self.device_info = DeviceInfo(self)
        self.device_profile = DeviceProfile(self)
        
        self.device_connection.connected.connect(
            self.device_connected
        )

        self.device_connection.disconnected.connect(
            self.device_disconnected
        )

        content = QHBoxLayout()
        content.setSpacing(20)

        left = QVBoxLayout()
        left.setSpacing(20)

        left.addWidget(self.device_connection)
        left.addWidget(self.device_info)
        left.addStretch()

        content.addLayout(left, 55)
        content.addWidget(self.device_profile, 45, Qt.AlignmentFlag.AlignTop)

        layout.addLayout(content)
        layout.addStretch()

    def device_connected(self, _, info):
        self.device_info.set_device_info(
            chip=info["chip"],
            uid=info["uid"]
        )
        
        self.device_profile.load_profile(
            info["chip"]
        )
        
    def device_disconnected(self):
        self.device_info.clear()
        self.device_profile.show_empty()