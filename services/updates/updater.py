
import os
import sys
import time
import subprocess
from pathlib import Path

def replace_executable(old_exe, new_exe, parent_pid):
    old_exe = Path(old_exe).resolve()
    new_exe = Path(new_exe).resolve()

    if old_exe.name.lower() != "plantera.exe":
        raise ValueError("Invalid application executable")

    if not old_exe.is_file() or not new_exe.is_file():
        raise FileNotFoundError("Update files not found")

    if old_exe == new_exe:
        raise ValueError("Source and destination are identical")

    backup_exe = old_exe.with_name("PlantERA.exe.bak")

    # Изчакваме основното приложение да се затвори
    import ctypes

    SYNCHRONIZE = 0x00100000
    WAIT_OBJECT_0 = 0
    WAIT_TIMEOUT = 0x00000102

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    handle = kernel32.OpenProcess(
        SYNCHRONIZE, False, parent_pid
    )

    if handle:
        result = kernel32.WaitForSingleObject(handle, 60000)
        kernel32.CloseHandle(handle)

        if result == WAIT_TIMEOUT:
            raise TimeoutError("PlantERA did not close")

        if result != WAIT_OBJECT_0:
            raise RuntimeError("Failed to wait for PlantERA")

    # Запазваме старата версия
    if backup_exe.exists():
        backup_exe.unlink()

    for attempt in range(20):
        try:
            os.replace(old_exe, backup_exe)
            break
        except PermissionError:
            if attempt == 19:
                raise
            time.sleep(1)

    try:
        # Инсталираме новата версия
        os.replace(new_exe, old_exe)

        # Стартираме обновеното приложение
        subprocess.Popen(
            [str(old_exe)],
            cwd=str(old_exe.parent)
        )

    except Exception:
        # Възстановяваме старата версия
        if backup_exe.exists():
            os.replace(backup_exe, old_exe)
        raise


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(1)

    replace_executable(
        sys.argv[1],
        sys.argv[2],
        int(sys.argv[3])
    )
