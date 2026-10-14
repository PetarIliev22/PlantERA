import sys
import time

START_TIME = time.perf_counter()

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

    app.setFont(QFont("Inter", 10))
    
    app.setStyleSheet(
        load_styles()
    )

    window = MainWindow()
    window.show()
    
    startup_time = time.perf_counter() - START_TIME
    print(
        f"Startup time: {startup_time:.3f} seconds"
    )


    sys.exit(app.exec())