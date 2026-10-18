
import sys
import time
import asyncio
import ctypes

START_TIME = time.perf_counter()

from qasync import QEventLoop
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase, QIcon
from ui.main_window import MainWindow
from utils.paths import resource_path
from styles.style_loader import load_styles

if __name__ == "__main__":

    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "PlantERA.Desktop.App"
        )

    app = QApplication(sys.argv)

    app.setWindowIcon(
        QIcon(str(resource_path("assets", "img", "logo", "plantera_logo.ico")))
    )

    QFontDatabase.addApplicationFont(
        str(resource_path("assets", "fonts", "Inter-Regular.ttf"))
    )
    
    app.setFont(QFont("Inter", 10))

    app.setStyleSheet(load_styles())

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.setWindowIcon(app.windowIcon())
    window.show()

    startup_time = time.perf_counter() - START_TIME
    print(f"Startup time: {startup_time:.3f} seconds")

    app.aboutToQuit.connect(loop.stop)

    with loop:
        loop.run_forever()
