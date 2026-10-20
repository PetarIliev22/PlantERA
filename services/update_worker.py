
from PySide6.QtCore import QThread, Signal

from services.update_service import (
    check_for_updates,
    download_update,
    get_update_checksum
)

class UpdateWorker(QThread):
    update_available = Signal(dict)
    progress_changed = Signal(int)
    download_finished = Signal(str)
    download_failed = Signal(str)

    def __init__(self, download: bool = False, update=None, parent=None):
        super().__init__(parent)

        self.download = download
        self.update = update

    def run(self):
        if not self.download:
            update = check_for_updates()

            if update:
                self.update_available.emit(update)

        else:
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
