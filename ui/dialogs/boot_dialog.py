import customtkinter as ctk
import subprocess
import sys
import threading
import re


class BootDialog(ctk.CTkFrame):
    def __init__(self, parent, port, on_connected):
        super().__init__(
            parent,
            fg_color="#E9EEF3",
            corner_radius=0
        )

        self.port = port
        self.on_connected = on_connected
        self.running = True

        self.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        self.lift()

        # Modal card
        self.card = ctk.CTkFrame(
            self,
            width=460,
            height=360,
            corner_radius=18,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#D9E1EA"
        )
        self.card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )
        self.card.pack_propagate(False)

        # BOOT icon
        self.boot_icon = ctk.CTkLabel(
            self.card,
            text="BOOT",
            width=70,
            height=70,
            corner_radius=35,
            fg_color="#EAF4FF",
            text_color="#1687F8",
            font=ctk.CTkFont("Arial", 14, "bold")
        )
        self.boot_icon.pack(pady=(35, 18))

        # Title
        self.title_label = ctk.CTkLabel(
            self.card,
            text="Hold the BOOT button",
            font=ctk.CTkFont("Arial", 21, "bold"),
            text_color="#172033"
        )
        self.title_label.pack()

        # Description
        self.description = ctk.CTkLabel(
            self.card,
            text=(
                "Press and hold BOOT on the ESP32.\n"
                "Keep holding until the device is detected."
            ),
            font=ctk.CTkFont("Arial", 14),
            text_color="#738199",
            justify="center"
        )
        self.description.pack(pady=(10, 20))

        # Status
        self.status_label = ctk.CTkLabel(
            self.card,
            text="●  Waiting for ESP32...",
            font=ctk.CTkFont("Arial", 14, "bold"),
            text_color="#1687F8"
        )
        self.status_label.pack(pady=(5, 20))

        # Cancel
        self.cancel_button = ctk.CTkButton(
            self.card,
            text="Cancel",
            width=110,
            height=36,
            corner_radius=9,
            fg_color="#F4F7FA",
            hover_color="#EAF4FF",
            border_width=1,
            border_color="#D9E1EA",
            text_color="#172033",
            command=self.cancel
        )
        self.cancel_button.pack()

        # Start detection
        threading.Thread(
            target=self.detect_esp32,
            daemon=True
        ).start()

    def detect_esp32(self):
        print(f"Waiting for ESP32 on {self.port}...")

        while self.running:
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

                if "Connected to ESP32" in output:
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

                    self.after(
                        0,
                        lambda: self.device_detected(
                            chip,
                            mac,
                            uid
                        )
                    )

                    return

            except subprocess.TimeoutExpired:
                pass

            except Exception as error:
                print(f"Detection error: {error}")

    def create_uid(self, mac):
        if mac == "Unknown":
            return "Unknown"

        # Match ESP.getEfuseMac() formatting used by firmware
        parts = mac.split(":")
        parts.reverse()

        return "PC-" + "".join(parts)

    def device_detected(self, chip, mac, uid):
        if not self.winfo_exists():
            return

        self.boot_icon.configure(
            text="✓",
            fg_color="#E9F8F1",
            text_color="#22B573",
            font=ctk.CTkFont("Arial", 30, "bold")
        )

        self.title_label.configure(
            text="ESP32 detected"
        )

        self.description.configure(
            text="You can release the BOOT button."
        )

        self.status_label.configure(
            text="●  Device connected",
            text_color="#22B573"
        )

        self.on_connected()

    def cancel(self):
        self.running = False
        self.destroy()