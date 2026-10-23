
import sys
import json
import subprocess

from pathlib import Path
from services.updates.update_worker import UpdateWorker

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar
)

class UpdaterWindow(QWidget):
    def __init__(self, update=None):
        super().__init__()
        self.update = update
        self.worker = None
        
        self.setWindowTitle("PlantERA Launcher")
        self.setFixedSize(420, 180)

        layout = QVBoxLayout(self)

        self.title = QLabel("PlantERA Updater")
        self.status = QLabel("Ready to update")

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        layout.addWidget(self.title)
        layout.addWidget(self.status)
        layout.addWidget(self.progress)

        if self.update:
            self.start_download()
        
    def set_status(self, message):
        self.status.setText(message)

    def set_progress(self, value):
        self.progress.setValue(value)

    def start_download(self):
        self.set_status("Downloading update...")

        self.worker = UpdateWorker(
            download=True,
            update=self.update,
            parent=self
        )

        self.worker.progress_changed.connect(self.set_progress)
        self.worker.download_finished.connect(self.on_download_finished)
        self.worker.download_failed.connect(self.on_download_failed)

        self.worker.start()

    def on_download_finished(self, exe_path):
        self.set_progress(100)
        self.set_status("Update downloaded and verified.")

    def on_download_failed(self, error):
        self.set_status(f"Update failed: {error}")


def launch_updater(update):
    command = [
        sys.executable,
        "-m",
        "ui.windows.updater_window",
        json.dumps(update)
    ]

    subprocess.Popen(
        command,
        cwd=str(Path(__file__).resolve().parents[2])
    )

if __name__ == "__main__":
    app = QApplication(sys.argv)

    update = json.loads(sys.argv[1]) if len(sys.argv) > 1 else None

    window = UpdaterWindow(update)
    window.show()

    sys.exit(app.exec())