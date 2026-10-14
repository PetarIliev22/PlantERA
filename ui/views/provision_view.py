
from ui.PySide6_Qt import *

from ui.components.provision.device_connection import DeviceConnection
from ui.components.provision.device_info import DeviceInfo
from ui.components.provision.device_profile import DeviceProfile
from ui.components.provision.device_actions import DeviceActions
from ui.components.provision.device_console import DeviceConsole


class ProvisionView(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName("provisionView")

        self.create_ui()
        self.connect_signals()
        self.fade_in()
        
        self.device_console.log("app_ready")

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.device_connection = DeviceConnection(self)
        self.device_info = DeviceInfo(self)
        self.device_profile = DeviceProfile(self)
        self.device_actions = DeviceActions(self)
        self.device_console = DeviceConsole(self)

        self.scroll = QScrollArea(self)
        self.scroll.setObjectName("provisionScroll")

        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.scroll.setMinimumSize(0, 0)

        container = QWidget()
        container.setObjectName("provisionContainer")

        content_layout = QVBoxLayout(container)
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(10)

        content_layout.setSizeConstraint(
            QLayout.SizeConstraint.SetMinimumSize
        )

        content_layout.addLayout(self.create_content())
        content_layout.addWidget(self.device_actions)
        content_layout.addWidget(self.device_console)
        content_layout.addStretch(1)

        self.scroll.setWidget(container)
        layout.addWidget(self.scroll)

    def create_content(self):
        content = QHBoxLayout()
        content.setSpacing(20)

        left = QVBoxLayout()
        left.setSpacing(20)

        left.addWidget(self.device_connection)
        left.addWidget(self.device_info)

        content.addLayout(left, 55)

        content.addWidget(
            self.device_profile,
            45,
            Qt.AlignmentFlag.AlignTop
        )

        return content

    def connect_signals(self):
        self.device_connection.connected.connect(
            self.device_connected
        )

        self.device_connection.disconnected.connect(
            self.device_disconnected
        )
        
        self.device_connection.connection_failed.connect(
            self.device_connection_failed
        )

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

    
    def device_connected(self, port, info):
        self.device_info.set_device_info(
            chip=info["chip"],
            uid=info["uid"]
        )

        self.device_profile.load_profile(
            info["chip"]
        )

        self.device_console.log(
            "connected",
            "SUCCESS",
            port=port
        )

        self.device_console.log(
            "device_info_loaded",
            "SUCCESS"
        )

        self.device_console.log(
            "chip_detected",
            "INFO",
            chip=info["chip"]
        )


    def device_disconnected(self):
        self.device_info.clear()
        self.device_profile.show_empty()

        self.device_console.log(
            "disconnected",
            "WARNING"
        )


    def device_connection_failed(self, message):
        self.device_console.append_log(
            message,
            "ERROR"
        )
