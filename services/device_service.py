import time
import threading

from esptool.cmds import detect_chip
from ui.PySide6_Qt import *

class DeviceService(QObject):
    detected = Signal(dict)
    failed = Signal()

    def __init__(self):
        super().__init__()
        self.stop_event = False

    def start(self, port):
        self.stop_event = threading.Event()
        threading.Thread(
            target=self.detect,
            args=(port, self.stop_event),
            daemon=True
        ).start()

    def stop(self):
        if self.stop_event:
            self.stop_event.set()

    def detect(self, port, stop_event):
        start_time = time.time()

        while not stop_event.is_set():
            if time.time() - start_time > 15:
                if not stop_event.is_set():
                    self.failed.emit()
                return

            try:
                with detect_chip(port) as esp:
                    if stop_event.is_set():
                        return
                    
                    board = esp.get_chip_description()
                    mac = esp.read_mac()

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