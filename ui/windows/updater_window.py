import os
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
        self.downloaded_files = None
        
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
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    def on_download_finished(self, downloaded_files):
        self.set_progress(100)
        self.set_status("Update downloaded and verified.")
        self.downloaded_files = downloaded_files

    def on_download_failed(self, error):
        self.set_status(f"Update failed: {error}")

    def on_worker_finished(self):
        if self.downloaded_files is None:
            return

        installed_exe = self.update.get("installed_exe")

        if not installed_exe:
            self.set_status("Installation requires the packaged application.")
            return

        app_name = Path(installed_exe).name

        app_file = next(
            (item for item in self.downloaded_files
            if item["asset"]["name"] == app_name),
            None
        )

        updater_file = next(
            (item for item in self.downloaded_files
            if item["asset"]["name"] != app_name),
            None
        )

        if not app_file or not updater_file:
            self.set_status("Required update files are missing.")
            return

        try:
            subprocess.Popen([
                str(updater_file["path"]),
                installed_exe,
                str(app_file["path"]),
                str(os.getpid())
            ])

        except OSError as error:
            self.set_status(f"Installation failed: {error}")
            return

        QApplication.instance().quit()
        

def launch_updater(update):
    if getattr(sys, "frozen", False):
        update = {
            **update,
            "installed_exe": str(Path(sys.executable).resolve())
        }

        command = [
            sys.executable,
            "--updater-window",
            json.dumps(update)
        ]
    else:
        command = [
            sys.executable,
            "-m",
            "ui.windows.updater_window",
            json.dumps(update)
        ]

    subprocess.Popen(
        command,
        cwd=str(Path(__file__).resolve().parents[2])
        if not getattr(sys, "frozen", False)
        else str(Path(sys.executable).resolve().parent)
    )

if __name__ == "__main__":
    app = QApplication(sys.argv)

    update = json.loads(sys.argv[1]) if len(sys.argv) > 1 else None

    window = UpdaterWindow(update)
    window.show()

    sys.exit(app.exec())