import json
from enum import Enum

from ui.PySide6_Qt import *
from services.device_service import DeviceService

texts = json.load(
    open("config/boot_dialog.json", encoding="utf-8")
)

class State(Enum):
    WAITING = "waiting"
    SUCCESS = "success"
    FAILED = "failed"

class BootDialog(QFrame):
    def __init__(self, parent, port, on_connected):
        super().__init__(parent)

        self.port = port
        self.on_connected = on_connected

        self.service = DeviceService()
        self.service.detected.connect(self.device_detected)
        self.service.failed.connect(self.connection_failed)

        self.setObjectName("bootOverlay")
        self.setGeometry(parent.rect())

        self.create_ui()
        self.set_state(State.WAITING)

        self.raise_()
        self.show()

        self.service.start(self.port)

    def create_ui(self):
        self.card = QFrame(self)
        self.card.setObjectName("bootCard")
        self.card.setFixedSize(460, 360)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(0, 35, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.boot_icon = QLabel()
        self.boot_icon.setObjectName("bootIcon")
        self.boot_icon.setFixedSize(70, 70)
        self.boot_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel()
        self.title_label.setObjectName("bootTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.description = QLabel()
        self.description.setObjectName("bootDescription")
        self.description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel()
        self.status_label.setObjectName("bootStatus")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button = QPushButton()
        self.button.setObjectName("bootButton")
        self.button.setFixedSize(110, 36)

        layout.addWidget(
            self.boot_icon,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        layout.addSpacing(18)

        layout.addWidget(self.title_label)
        layout.addSpacing(10)

        layout.addWidget(self.description)
        layout.addSpacing(20)

        layout.addWidget(self.status_label)
        layout.addSpacing(20)

        layout.addWidget(
            self.button,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )

    def set_state(self, state):
        data = texts[state.value]

        icons = {
            State.WAITING: "BOOT",
            State.SUCCESS: "✓",
            State.FAILED: "!"
        }

        self.boot_icon.setText(icons[state])
        self.title_label.setText(data["title"])
        self.description.setText(data["description"])
        self.status_label.setText(data["status"])

        self.boot_icon.setProperty("state", state.value)
        self.status_label.setProperty("state", state.value)

        self.button.setText(data.get("button", "Cancel"))

        self.set_button_action(
            self.try_again
            if state == State.FAILED
            else self.cancel
        )

        self.refresh_style()

    def device_detected(self, info):
        print(info)
        self.set_state(State.SUCCESS)
        self.on_connected(info)

    def connection_failed(self):
        self.set_state(State.FAILED)

    def try_again(self):
        self.set_state(State.WAITING)
        self.service.start(self.port)

    def cancel(self):
        self.service.stop()
        self.deleteLater()

    def set_button_action(self, action):
        try:
            self.button.clicked.disconnect()
        except RuntimeError:
            pass

        self.button.clicked.connect(action)

    def refresh_style(self):
        for widget in (self.boot_icon, self.status_label):
            widget.style().unpolish(widget)
            widget.style().polish(widget)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.card.move(
            (self.width() - self.card.width()) // 2,
            (self.height() - self.card.height()) // 2
        )