from ui.PySide6_Qt import *
from config.version import APP_VERSION
from services.update_worker import UpdateWorker
from config.config_loader import load_config

texts = load_config("update_dialog.json")

class UpdateDialog(QFrame):
    def __init__(self, parent, update):
        super().__init__(parent)

        self.update = update
        self.worker = None

        self.setObjectName("updateOverlay")
        self.setGeometry(parent.rect())

        self.card = QFrame(self)
        self.card.setObjectName("updateDialog")
        self.card.setFixedWidth(520)
        
        overlay_layout = QVBoxLayout(self)
        overlay_layout.addWidget(self.card,alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout = QVBoxLayout(self.card)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Title
        self.title = QLabel(texts["title"].format(version=update["version"]))
        self.title.setObjectName("updateTitle")

        # Description
        self.description = QLabel(texts["description"].format(current_version=APP_VERSION))
        self.description.setObjectName("updateDescription")

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setObjectName("updateProgress")
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.hide()
        
        # Status
        self.status_label = QLabel()
        self.status_label.setObjectName("updateStatus")
        self.status_label.setWordWrap(True)
        self.status_label.hide()
        
        # Update button
        self.update_button = QPushButton(texts["buttons"]["update"])
        self.update_button.setObjectName("updateButton")
        self.update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.update_button.clicked.connect(self.start_download)

        # Layout
        layout.addWidget(self.title)
        layout.addWidget(self.description)
        layout.addSpacing(10)
        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)
        layout.addWidget(self.update_button)

    def start_download(self):
        self.update_button.setEnabled(False)
        self.update_button.setText(texts["buttons"]["downloading"])
        self.progress.show()
        
        self.worker = UpdateWorker(download=True,update=self.update,parent=self)

        self.worker.progress_changed.connect(self.progress.setValue)
        self.worker.download_finished.connect(self.on_download_finished)
        self.worker.download_failed.connect(self.on_download_failed)
        self.worker.finished.connect(self.on_worker_finished)

        self.worker.start()

    def on_download_finished(self, exe_path):
        self.progress.setValue(100)
        self.update_button.setText(texts["buttons"]["downloaded"])

        self.set_status(texts["messages"]["download_success"],"success")

    def on_download_failed(self, error):
        self.update_button.setText(texts["buttons"]["retry"])
        self.set_status(str(error), "error")

    def on_worker_finished(self):
        if self.update_button.text() == texts["buttons"]["retry"]:
            self.update_button.setEnabled(True)

    def closeEvent(self, event):
        if self.worker is not None and self.worker.isRunning():
            self.set_status(
                texts["messages"]["download_in_progress"],
                "info"
            )
            event.ignore()
            return

        super().closeEvent(event)

    def set_status(self, message, status):
        self.status_label.setText(message)
        self.status_label.setProperty("status", status)

        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

        self.status_label.show()

def show_update_dialog(parent, update):
    dialog = UpdateDialog(parent, update)
    dialog.setGeometry(parent.rect())
    dialog.raise_()
    dialog.show()

    return dialog