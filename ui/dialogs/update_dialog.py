
from ui.PySide6_Qt import *

from config.version import APP_VERSION
from services.update_service import (
    download_update,
    get_update_checksum
)

class DownloadWorker(QThread):
    progress_changed = Signal(int)
    download_finished = Signal(str)
    download_failed = Signal(str)

    def __init__(self, update, parent=None):
        super().__init__(parent)
        self.update = update

    def run(self):
        try:
            checksum = get_update_checksum(self.update)

            exe_path = download_update(
                self.update["download_url"],
                checksum,
                self.progress_changed.emit
            )

            self.download_finished.emit(str(exe_path))

        except Exception as error:
            self.download_failed.emit(str(error))


class UpdateDialog(QDialog):
    def __init__(self, parent, update):
        super().__init__(parent)

        self.update = update
        self.worker = None

        self.setObjectName("updateDialog")
        self.setWindowTitle("PlantERA Update")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Title
        self.title = QLabel(
            f"PlantERA v{update['version']} is available"
        )
        self.title.setObjectName("updateTitle")

        # Description
        self.description = QLabel(
            f"Current version: {APP_VERSION}"
        )
        self.description.setObjectName("updateDescription")

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setObjectName("updateProgress")
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.hide()

        # Update button
        self.update_button = QPushButton("Update now")
        self.update_button.setObjectName("updateButton")
        self.update_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.update_button.clicked.connect(
            self.start_download
        )

        # Layout
        layout.addWidget(self.title)
        layout.addWidget(self.description)
        layout.addSpacing(10)
        layout.addWidget(self.progress)
        layout.addWidget(self.update_button)

    def start_download(self):
        self.update_button.setEnabled(False)
        self.update_button.setText("Downloading...")
        self.progress.show()

        self.worker = DownloadWorker(self.update, self)

        self.worker.progress_changed.connect(
            self.progress.setValue
        )

        self.worker.download_finished.connect(
            self.on_download_finished
        )

        self.worker.download_failed.connect(
            self.on_download_failed
        )

        self.worker.start()

    def on_download_finished(self, exe_path):
        self.progress.setValue(100)
        self.update_button.setText("Downloaded")

        QMessageBox.information(
            self,
            "PlantERA Update",
            "Update downloaded and verified successfully.\n\n"
            "Installation will be added in the next step."
        )

    def on_download_failed(self, error):
        self.update_button.setEnabled(True)
        self.update_button.setText("Try again")

        QMessageBox.warning(
            self,
            "Update Failed",
            str(error)
        )

    def closeEvent(self, event):
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(
                self,
                "PlantERA Update",
                "Please wait until the download finishes."
            )
            event.ignore()
            return

        super().closeEvent(event)


def show_update_dialog(parent, update):
    dialog = UpdateDialog(parent, update)
    dialog.exec()
