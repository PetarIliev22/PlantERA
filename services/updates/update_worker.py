from pathlib import Path
from PySide6.QtCore import QThread, Signal
from services.updates.update_service import (
    check_for_updates,
    download_update,
    get_update_checksum
)

class UpdateWorker(QThread):
    update_available = Signal(dict)
    progress_changed = Signal(int)
    download_finished = Signal(list)
    download_failed = Signal(str)

    def __init__(self, download: bool = False, update=None, parent=None):
        super().__init__(parent)

        self.download = download
        self.update = update

    def run(self):
        if self.download:
            self.download_files()
        else:
            self.check_update()

    def check_update(self):
        update = check_for_updates()

        if update:
            self.update_available.emit(update)

    def download_files(self):
        downloaded_files = []
        
        try:
            required = {"PlantERA.exe", "PlantERAUpdater.exe"}
            assets = [
                asset for asset in self.update["assets"]
                if asset["name"] in required
            ]

            found = {asset["name"] for asset in assets}

            if found != required or len(assets) != 2:
                raise RuntimeError("Required update files are missing")

            for index, asset in enumerate(assets):
                checksum = get_update_checksum(self.update, asset)

                def on_progress(progress, index=index):
                    total = (index + progress / 100) / len(assets) * 100
                    self.progress_changed.emit(int(total))

                path = download_update(
                    asset,
                    checksum,
                    on_progress
                )

                downloaded_files.append({
                    "asset": asset,
                    "path": path
                })

            self.progress_changed.emit(100)
            self.download_finished.emit(downloaded_files)

        except Exception as error:
            for item in downloaded_files:
                path = Path(item["path"])

                try:
                    path.unlink(missing_ok=True)
                    path.parent.rmdir()
                except OSError:
                    pass

            self.download_failed.emit(str(error))
