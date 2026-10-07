import sys

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from styles.style_loader import load_styles

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyleSheet(
        load_styles()
    )

    window = MainWindow()
    window.show()

    sys.exit(app.exec())