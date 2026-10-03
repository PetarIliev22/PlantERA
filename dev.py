import subprocess
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class ReloadHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.restart()

    def restart(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

        self.process = subprocess.Popen(
            [sys.executable, "main.py"]
        )

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print("Промяна открита -> рестартиране...")
            self.restart()


handler = ReloadHandler()

observer = Observer()
observer.schedule(
    handler,
    path=".",
    recursive=True
)

observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

    if handler.process:
        handler.process.terminate()

observer.join()