import sys

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from ui.main_window import MainWindow
from utils.paths import resource_path
from styles.style_loader import load_styles

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    QFontDatabase.addApplicationFont(
        str(resource_path("assets", "fonts", "Inter-Regular.ttf"))
    )

    app.setFont(
        QFont("Inter", 10)
    )
    
    app.setStyleSheet(
        load_styles()
    )

    window = MainWindow()
    window.show()

    sys.exit(app.exec())