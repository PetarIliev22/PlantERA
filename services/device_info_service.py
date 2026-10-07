import re
import sys
import subprocess


class DeviceInfoService:
    def read(self, port):
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

        if result.returncode != 0:
            return None

        output = result.stdout + result.stderr

        chip = self.find(
            r"Chip type:\s+(.+)",
            output
        )

        mac = self.find(
            r"MAC:\s+([0-9a-fA-F:]{17})",
            output
        ).upper()

        return {
            "board": chip,
            "uid": self.create_uid(mac)
        }

    @staticmethod
    def find(pattern, output):
        match = re.search(pattern, output)

        return (
            match.group(1).strip()
            if match
            else "Not available"
        )

    @staticmethod
    def create_uid(mac):
        if mac == "NOT AVAILABLE":
            return "Not available"

        return "PC-" + "".join(
            reversed(mac.split(":"))
        )