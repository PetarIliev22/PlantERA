import os
import shutil
import tempfile
import threading

from pathlib import Path

def cleanup_completed_update():
    folder = os.environ.pop("PLANTERA_UPDATE_DIR", None)
    pid = os.environ.pop("PLANTERA_UPDATER_PID", None)

    if not folder or not pid:
        return

    try:
        updater_pid = int(pid)
        update_dir = Path(folder).resolve()
        temp_dir = Path(tempfile.gettempdir()).resolve()

        if (
            update_dir.parent != temp_dir
            or not update_dir.name.startswith("plantera_update_")
            or update_dir.is_symlink()
        ):
            return

    except (ValueError, OSError):
        return

    def cleanup():
        try:
            from services.updates.updater import wait_for_process
            wait_for_process(updater_pid)

            shutil.rmtree(update_dir)

        except (OSError, TimeoutError, ValueError):
            pass

    threading.Thread(
        target=cleanup,
        daemon=True
    ).start()