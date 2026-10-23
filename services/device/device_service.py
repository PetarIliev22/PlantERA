import time
import logging
import threading

from PySide6.QtCore import QObject, Signal

logger = logging.getLogger(__name__)

class DeviceService(QObject):
    detected = Signal(dict)
    failed = Signal()

    DETECTION_TIMEOUT = 5.0
    RETRY_INTERVAL = 0.2
    
    def __init__(self):
        super().__init__()
        self.stop_event = None
        self.worker_thread = None
        
    @property
    def is_running(self):
        return (
            self.worker_thread is not None
            and self.worker_thread.is_alive()
        )

    def start(self, port):
        if self.is_running:
            return False

        self.stop_event = threading.Event()
    
        self.worker_thread = threading.Thread(
            target=self.detect,
            args=(port, self.stop_event),
            daemon=True
        )
        
        self.worker_thread.start()
        return True

    def stop(self):
        if self.stop_event is not None:
            self.stop_event.set()
            

    def detect(self, port, stop_event):
        from esptool.cmds import detect_chip
        
        deadline = (
            time.monotonic() + self.DETECTION_TIMEOUT
        )
        
        last_error = None
        while not stop_event.is_set():
            if time.monotonic() > deadline:
                self.failed.emit()
                return

            try:
                with detect_chip(port, connect_attempts=1) as esp:
                    if stop_event.is_set():
                        return
                    
                    info = {
                        "chip": esp.get_chip_description(),
                        "uid": self.create_uid(esp.read_mac())
                    }
                    
                    if not stop_event.is_set():
                        self.detected.emit(info)

                    return

            except Exception as e:
                message = str(e)

                if message != last_error:
                    logger.warning(
                        "ESP32 detection failed: %s",
                        message
                    )
                last_error = message

            if stop_event.wait(self.RETRY_INTERVAL):
                return

    @staticmethod
    def create_uid(mac):
        return "PC-" + "".join(
            f"{byte:02X}"
            for byte in reversed(mac)
        )