import time
import threading

from PySide6.QtCore import QObject, Signal
class DeviceService(QObject):
    detected = Signal(dict)
    failed = Signal()

    def __init__(self):
        super().__init__()
        self.stop_event = None

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
        from esptool.cmds import detect_chip
        start_time = time.time()    
        last_error = None
        
        while not stop_event.is_set():
            if time.time() - start_time > 15:
                self.failed.emit()
                return

            try:
                with detect_chip(port) as esp:
                    if stop_event.is_set():
                        return
                    
                    chip = esp.get_chip_description()
                    mac = esp.read_mac()

                    self.detected.emit({
                        "chip": chip,
                        "uid": self.create_uid(mac)
                    })

                    return

            except Exception as e:
                error = str(e)

                if error != last_error:
                    print(f"[DeviceService] Detection error: {error}")
                    last_error = error

                time.sleep(0.2)

    @staticmethod
    def create_uid(mac):
        return "PC-" + "".join(
            f"{byte:02X}"
            for byte in reversed(mac)
        )