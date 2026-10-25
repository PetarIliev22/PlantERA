import os
import sys
import json
import subprocess

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QProgressBar, QVBoxLayout, QHBoxLayout
)

from services.updates.update_worker import UpdateWorker
from utils.paths import resource_path
from config.version import APP_NAME, APP_VERSION

class UpdaterWindow(QWidget):
    def __init__(self, update=None):
        super().__init__()

        self.update = update
        self.worker = None
        self.downloaded_files = None

        self.setObjectName("updaterWindow")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(420, 180)

        self.setup_ui()

        if update:
            self.start_download()

    def setup_ui(self):
        def label(text, name):
            widget = QLabel(text)
            widget.setObjectName(name)
            return widget

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 16, 22, 16)
        layout.setSpacing(12)

        header = QHBoxLayout()

        logo = label("", "updateLogo")
        logo.setFixedSize(46, 46)

        image = QPixmap(str(resource_path(
            "assets", "img", "logo", "plantera_logo.png"
        )))
        logo.setPixmap(image.scaled(
            42, 42, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))

        heading = QVBoxLayout()
        heading.addWidget(label(APP_NAME, "updateTitle"))
        heading.addWidget(label("Software Update", "updateSubtitle"))

        version = self.update["version"] if self.update else APP_VERSION
        self.version = label(f"v{version}", "updateVersion")

        header.addWidget(logo)
        header.addLayout(heading)
        header.addStretch()
        header.addWidget(self.version)

        layout.addLayout(header)
        layout.addStretch()

        status = QHBoxLayout()
        self.status = label("Ready to update", "updateStatus")
        self.percentage = label("0%", "updatePercentage")
        status.addWidget(self.status, 1)
        status.addWidget(self.percentage)
        layout.addLayout(status)

        self.progress = QProgressBar()
        self.progress.setObjectName("updateProgress")
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(8)
        layout.addWidget(self.progress)

        footer = QHBoxLayout()
        self.verification_label = label("Preparing installation...", "updateFooter")
        footer.addWidget(self.verification_label)
        footer.addStretch()

        self.hint = label("Automatic installation", "updateFooter")
        footer.addWidget(self.hint)
        layout.addLayout(footer)

    def set_status(self, message):
        self.status.setText(message)
        self.status.setToolTip(message)

    def set_progress(self, value):
        self.progress.setValue(value)
        self.percentage.setText(f"{value}%")

    def start_download(self):
        self.set_status("Downloading update...")

        self.worker = UpdateWorker(True, self.update, self)
        self.worker.progress_changed.connect(self.set_progress)
        self.worker.download_finished.connect(self.on_download_finished)
        self.worker.download_failed.connect(self.on_download_failed)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    def on_download_finished(self, files):
        self.downloaded_files = files
        self.verification_label.setText("✓ Download complete")
        self.set_progress(100)
        self.set_status("Download verified.")

    def on_download_failed(self, error):
        self.set_status(f"Update failed: {error}")
        self.hint.setText("Installation cancelled")

    def cleanup_downloads(self):
        import shutil

        if self.downloaded_files:
            folder = Path(self.downloaded_files[0]["path"]).parent
            shutil.rmtree(folder, ignore_errors=True)

    def on_worker_finished(self):
        if not self.downloaded_files:
            return

        installed = self.update.get("installed_exe")

        if not installed:
            self.set_status("Installation requires packaged app.")
            self.cleanup_downloads()
            return

        files = {
            item["asset"]["name"]: item["path"]
            for item in self.downloaded_files
        }

        app = files.get(Path(installed).name)
        updater = files.get(f"{APP_NAME}Updater.exe")

        if not app or not updater:
            self.set_status("Required update files are missing.")
            self.cleanup_downloads()
            return

        self.set_status("Installing update...")
        self.hint.setText("PlantERA will restart")

        try:
            subprocess.Popen([
                str(updater), installed, str(app), str(os.getpid())
            ])
        except OSError as error:
            self.set_status(f"Installation failed: {error}")
            self.cleanup_downloads()
            return

        QApplication.instance().quit()

def launch_updater(update):
    frozen = getattr(sys, "frozen", False)

    if frozen:
        update = {
            **update,
            "installed_exe": str(Path(sys.executable).resolve())
        }

    command = (
        [sys.executable, "--updater-window", json.dumps(update)]
        if frozen else
        [sys.executable, "-m", "ui.windows.updater_window", json.dumps(update)]
    )

    cwd = (
        Path(sys.executable).resolve().parent
        if frozen else Path(__file__).resolve().parents[2]
    )

    env = os.environ.copy()

    if frozen:
        env["PYINSTALLER_RESET_ENVIRONMENT"] = "1"

    subprocess.Popen(command, cwd=str(cwd), env=env)
    
if __name__ == "__main__":
    from styles.style_loader import load_styles

    app = QApplication(sys.argv)
    app.setStyleSheet(load_styles())

    update = json.loads(sys.argv[1]) if len(sys.argv) > 1 else None
    window = UpdaterWindow(update)
    window.show()

    sys.exit(app.exec())
