
import os
import sys
import time
import ctypes
import subprocess

from pathlib import Path

def wait_for_process(pid):
    from ctypes import wintypes

    if pid <= 0:
        raise ValueError(f"Invalid application PID: {pid}")

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    SYNCHRONIZE = 0x00100000
    WAIT_OBJECT_0 = 0
    WAIT_TIMEOUT = 0x00000102
    ERROR_INVALID_PARAMETER = 87

    kernel32.OpenProcess.argtypes = [
        wintypes.DWORD,
        wintypes.BOOL,
        wintypes.DWORD
    ]
    kernel32.OpenProcess.restype = wintypes.HANDLE

    kernel32.WaitForSingleObject.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD
    ]
    kernel32.WaitForSingleObject.restype = wintypes.DWORD

    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL

    handle = kernel32.OpenProcess(SYNCHRONIZE, False, pid)

    if not handle:
        error = ctypes.get_last_error()

        if error == ERROR_INVALID_PARAMETER:
            return

        raise ctypes.WinError(error)

    try:
        result = kernel32.WaitForSingleObject(handle, 60000)

        if result == WAIT_TIMEOUT:
            raise TimeoutError("Application did not close")

        if result != WAIT_OBJECT_0:
            raise ctypes.WinError(ctypes.get_last_error())

    finally:
        kernel32.CloseHandle(handle)

def replace_executable(old_exe, new_exe, parent_pid):
    old_exe = Path(old_exe).resolve()
    new_exe = Path(new_exe).resolve()

    if not old_exe.is_file() or not new_exe.is_file():
        raise FileNotFoundError("Update files not found")

    if old_exe == new_exe:
        raise ValueError("Source and destination are identical")

    if old_exe.suffix.lower() != ".exe":
        raise ValueError("Invalid application executable")

    backup_exe = old_exe.with_suffix(".exe.bak")

    wait_for_process(parent_pid)

    for attempt in range(20):
        try:
            os.replace(old_exe, backup_exe)
            break
        except PermissionError:
            if attempt == 19:
                raise
            time.sleep(1)

    try:
        os.replace(new_exe, old_exe)

        subprocess.Popen(
            [str(old_exe)],
            cwd=str(old_exe.parent)
        )

    except Exception:
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
