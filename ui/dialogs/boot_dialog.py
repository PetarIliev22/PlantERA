import re
import sys
import time
import threading
import subprocess

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout
)


class BootDialog(QFrame):
    detected = Signal(str, str, str)
    failed = Signal()

    def __init__(self, parent, port, on_connected):
        super().__init__(parent)

        self.port = port
        self.on_connected = on_connected
        self.running = True

        self.setObjectName("bootOverlay")
        self.setGeometry(parent.rect())
        self.create_ui()
        
        self.raise_()
        self.show()

        self.detected.connect(self.device_detected)
        self.failed.connect(self.connection_failed)

        self.start_detection()

    def create_ui(self):
        # Modal card
        self.card = QFrame(self)
        self.card.setObjectName("bootCard")
        self.card.setFixedSize(460, 360)

        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(0, 35, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # BOOT icon
        self.boot_icon = QLabel("BOOT")
        self.boot_icon.setObjectName("bootIcon")
        self.boot_icon.setFixedSize(70, 70)
        self.boot_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.boot_icon.setProperty("state", "waiting")

        layout.addWidget(
            self.boot_icon,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )

        layout.addSpacing(18)

        # Title
        self.title_label = QLabel("Hold the BOOT button")
        self.title_label.setObjectName("bootTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.title_label)

        layout.addSpacing(10)

        # Description
        self.description = QLabel(
            "Press and hold BOOT on the ESP32.\n"
            "Keep holding until the device is detected."
        )
        self.description.setObjectName("bootDescription")
        self.description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.description)

        layout.addSpacing(20)

        # Status
        self.status_label = QLabel("●  Waiting for ESP32...")
        self.status_label.setObjectName("bootStatus")
        self.status_label.setProperty("state", "waiting")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.status_label)

        layout.addSpacing(20)

        # Cancel
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("bootButton")
        self.cancel_button.setFixedSize(110, 36)
        self.cancel_button.clicked.connect(self.cancel)

        layout.addWidget(
            self.cancel_button,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )

    def start_detection(self):
        self.running = True

        threading.Thread(
            target=self.detect_esp32,
            daemon=True
        ).start()

    def detect_esp32(self):
        start_time = time.time()

        print(f"Waiting for ESP32 on {self.port}...")

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
                        self.port,
                        "chip-id"
                    ],
                    capture_output=True,
                    text=True,
                    timeout=8
                )

                output = result.stdout + result.stderr

                if "Connected to ESP32" not in output:
                    continue

                self.running = False

                print("\n===== ESP32 DETECTED =====")
                print(output)

                chip_match = re.search(
                    r"Chip type:\s+(.+)",
                    output
                )

                mac_match = re.search(
                    r"MAC:\s+([0-9a-fA-F:]{17})",
                    output
                )

                chip = (
                    chip_match.group(1).strip()
                    if chip_match
                    else "Unknown"
                )

                mac = (
                    mac_match.group(1).upper()
                    if mac_match
                    else "Unknown"
                )

                uid = self.create_uid(mac)

                print("===== DEVICE INFO =====")
                print(f"Port: {self.port}")
                print(f"Chip: {chip}")
                print(f"MAC:  {mac}")
                print(f"UID:  {uid}")
                print("=======================\n")

                self.detected.emit(
                    chip,
                    mac,
                    uid
                )

                return

            except subprocess.TimeoutExpired:
                pass

            except Exception as error:
                print(f"Detection error: {error}")

    def create_uid(self, mac):
        if mac == "Unknown":
            return "Unknown"

        parts = mac.split(":")
        parts.reverse()

        return "PC-" + "".join(parts)

    def device_detected(self, chip, mac, uid):
        self.boot_icon.setText("✓")
        self.boot_icon.setProperty("state", "success")

        self.title_label.setText("ESP32 detected")

        self.description.setText(
            "You can release the BOOT button."
        )

        self.status_label.setText(
            "●  Device connected"
        )
        self.status_label.setProperty("state", "success")

        self.refresh_style(self.boot_icon)
        self.refresh_style(self.status_label)

        self.on_connected()

    def connection_failed(self):
        self.boot_icon.setText("!")
        self.boot_icon.setProperty("state", "failed")

        self.title_label.setText(
            "Connection failed"
        )

        self.description.setText(
            "ESP32 was not detected.\n"
            "Check the connection and try again."
        )

        self.status_label.setText(
            "●  Device not detected"
        )
        self.status_label.setProperty("state", "failed")

        self.cancel_button.setText("Try Again")

        try:
            self.cancel_button.clicked.disconnect()
        except RuntimeError:
            pass

        self.cancel_button.clicked.connect(
            self.try_again
        )

        self.refresh_style(self.boot_icon)
        self.refresh_style(self.status_label)

    def try_again(self):
        self.boot_icon.setText("BOOT")
        self.boot_icon.setProperty("state", "waiting")

        self.title_label.setText(
            "Hold the BOOT button"
        )

        self.description.setText(
            "Press and hold BOOT on the ESP32.\n"
            "Keep holding until the device is detected."
        )

        self.status_label.setText(
            "●  Waiting for ESP32..."
        )
        self.status_label.setProperty("state", "waiting")

        self.cancel_button.setText("Cancel")

        try:
            self.cancel_button.clicked.disconnect()
        except RuntimeError:
            pass

        self.cancel_button.clicked.connect(
            self.cancel
        )

        self.refresh_style(self.boot_icon)
        self.refresh_style(self.status_label)

        self.start_detection()

    def refresh_style(self, widget):
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def cancel(self):
        self.running = False
        self.deleteLater()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.card.move(
            (self.width() - 460) // 2,
            (self.height() - 360) // 2
        )