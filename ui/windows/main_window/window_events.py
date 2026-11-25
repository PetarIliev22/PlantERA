import sys
from ctypes import wintypes
from PySide6.QtCore import QTimer

class WindowEvents:
    def setup_timers(self):
        self.usb_timer = QTimer(self)
        self.usb_timer.setSingleShot(True)
        self.usb_timer.setInterval(300)
        self.usb_timer.timeout.connect(self.on_usb_changed)

    def on_usb_changed(self):
        if self.page_manager is None:
            return

        provision = self.page_manager.pages.get("provision")

        if provision is not None:
            provision.device_connection.refresh_ports()

    def nativeEvent(self, eventType, message):
        if sys.platform == "win32":
            msg = wintypes.MSG.from_address(int(message))

            if (
                msg.message == 0x0219
                and msg.wParam in (0x0007, 0x8000, 0x8004)
            ):
                self.usb_timer.start()

        return super().nativeEvent(eventType, message)
