import time
import threading

from esptool.cmds import detect_chip
from ui.PySide6_Qt import *

class DeviceService(QObject):
    detected = Signal(dict)
    failed = Signal()

    def __init__(self):
        super().__init__()
        self.running = False

    def start(self, port):
        self.running = True

        threading.Thread(
            target=self.detect,
            args=(port,),
            daemon=True
        ).start()

    def stop(self):
        self.running = False

    def detect(self, port):
        start_time = time.time()

        while self.running:
            if time.time() - start_time > 15:
                self.running = False
                self.failed.emit()
                return

            try:
                with detect_chip(port) as esp:
                    board = esp.get_chip_description()
                    mac = esp.read_mac()

                    self.running = False

                    self.detected.emit({
                        "board": board,
                        "uid": self.create_uid(mac)
                    })

                    return

            except Exception:
                pass

    @staticmethod
    def create_uid(mac):
        return "PC-" + "".join(
            f"{byte:02X}"
            for byte in reversed(mac)
        )