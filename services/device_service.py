import sys
import time
import threading
import subprocess

from ui.PySide6_Qt import *


class DeviceService(QObject):
    detected = Signal()
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
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "esptool",
                        "--port",
                        port,
                        "chip-id"
                    ],
                    capture_output=True,
                    text=True,
                    timeout=8
                )

                if result.returncode == 0:
                    self.running = False
                    self.detected.emit()
                    return

            except subprocess.TimeoutExpired:
                pass