from PySide6.QtCore import QTimer

class WindowUpdates:
    def start_update_check(self):
        from services.updates.update_worker import UpdateWorker

        self.update_worker = UpdateWorker(
            download=False,
            parent=self
        )

        self.update_worker.update_available.connect(
            self.on_update_available
        )
        self.update_worker.finished.connect(
            self.on_update_check_finished
        )

        self.update_worker.start()

    def on_update_available(self, update):
        if self._closing:
            return

        from ui.dialogs.update_dialog import show_update_dialog
        self.update_dialog = show_update_dialog(self, update)

    def on_update_check_finished(self):
        if self._closing:
            QTimer.singleShot(0, self.close)
