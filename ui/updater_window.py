
import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar
)

class UpdaterWindow(QWidget):
    def __init__(self):
        super().__init__()

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

    def set_status(self, message):
        self.status.setText(message)

    def set_progress(self, value):
        self.progress.setValue(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = UpdaterWindow()
    window.show()

    sys.exit(app.exec())
