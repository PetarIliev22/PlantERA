
import sys
import subprocess
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar
)

class UpdaterWindow(QWidget):
    def __init__(self, version=None):
        super().__init__()

        self.setWindowTitle("PlantERA Launcher")
        self.setFixedSize(420, 180)

        layout = QVBoxLayout(self)

        self.title = QLabel("PlantERA Updater")
        self.status = QLabel(
            f"Preparing PlantERA v{version}..."
            if version else "Ready to update"
        )

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        layout.addWidget(self.title)
        layout.addWidget(self.status)
        layout.addWidget(self.progress)

    def set_status(self, message):
        self.status.setText(message)

    def set_progress(self, value):
        self.progress.setValue(value)



def launch_updater(update):
    if getattr(sys, "frozen", False):
        updater_exe = Path(sys.executable).with_name("PlantERAUpdater.exe")

        if not updater_exe.is_file():
            raise FileNotFoundError("PlantERAUpdater.exe not found")

        command = [str(updater_exe), update["version"]]

    else:
        command = [
            sys.executable,
            "-m",
            "ui.updater_window",
            update["version"]
        ]

    subprocess.Popen(
        command,
        cwd=str(Path(sys.executable).parent) if getattr(sys, "frozen", False)
        else str(Path(__file__).resolve().parents[1])
    )

if __name__ == "__main__":
    app = QApplication(sys.argv)

    version = sys.argv[1] if len(sys.argv) > 1 else None

    window = UpdaterWindow(version)
    window.show()

    sys.exit(app.exec())
