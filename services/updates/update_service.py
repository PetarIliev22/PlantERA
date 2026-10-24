import time

from PySide6.QtCore import QSettings
from packaging.version import Version

from config.version import APP_NAME, APP_VERSION, GITHUB_RELEASES_API

CHECK_INTERVAL = 10 * 60
settings = QSettings("PlantERA", "PlantERA")

def create_request(url):
    import urllib.request
    
    return urllib.request.Request(
        url,
        headers={"User-Agent": "PlantERA-Updater"}
    )

def check_for_updates():
    import json
    import urllib.request
    from packaging.version import Version
    
    now = time.time()
    last_check = settings.value("last_update_check", 0, type=float)

    if now - last_check < CHECK_INTERVAL:
        return None

    try:
        with urllib.request.urlopen(
            create_request(GITHUB_RELEASES_API), timeout=5
        ) as response:
            release = json.load(response)

        version = release["tag_name"].removeprefix("v")
        assets = release.get("assets", [])

        if Version(version) <= Version(APP_VERSION):
            settings.setValue("last_update_check", now)
            return None

        app = next(
            (a for a in assets if a["name"] == f"{APP_NAME}.exe"),
            None
        )

        if not app:
            return None

        settings.setValue("last_update_check", now)

        return {
            "version": version,
            "download_url": app["browser_download_url"],
            "release_notes": release.get("body", ""),
            "assets": assets
        }

    except Exception as error:
        print(f"Update check failed: {error}")
        return None

def download_update(asset, expected_sha256, progress_callback=None):
    import hashlib
    import tempfile
    import urllib.request
    from pathlib import Path
    
    path = Path(tempfile.mkdtemp(prefix="plantera_update_"))
    file_path = path / Path(asset["name"]).name
    sha256 = hashlib.sha256()

    try:
        with urllib.request.urlopen(
            create_request(asset["browser_download_url"]), timeout=30
        ) as response, file_path.open("wb") as file:

            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0

            while chunk := response.read(1024 * 1024):
                file.write(chunk)
                sha256.update(chunk)
                downloaded += len(chunk)

                if progress_callback and total:
                    progress_callback(min(100, downloaded * 100 // total))

        if sha256.hexdigest().lower() != expected_sha256.lower():
            raise ValueError("Checksum mismatch")

        return file_path

    except Exception:
        file_path.unlink(missing_ok=True)
        path.rmdir()
        raise


def get_update_checksum(release, asset):
    import urllib.request
    
    checksum_file = next(
        (a for a in release["assets"] if a["name"] == "checksums.txt"),
        None
    )

    if not checksum_file:
        raise ValueError("Checksum file not found")

    with urllib.request.urlopen(
        create_request(checksum_file["browser_download_url"]),
        timeout=15
    ) as response:
        lines = response.read().decode("utf-8").splitlines()

    for line in lines:
        parts = line.split()

        if len(parts) == 2 and parts[1].lstrip("*") == asset["name"]:
            checksum = parts[0].lower()

            if len(checksum) == 64 and all(c in "0123456789abcdef" for c in checksum):
                return checksum

    raise ValueError("Invalid or missing checksum")

def cleanup_old_updates():
    import tempfile
    import shutil
    import time
    from pathlib import Path

    temp_dir = Path(tempfile.gettempdir())
    max_age = 24 * 60 * 60  # 24 hours
    now = time.time()

    for folder in temp_dir.glob("plantera_update_*"):
        try:
            if not folder.is_dir() or folder.is_symlink():
                continue

            age = now - folder.stat().st_mtime

            if age < max_age:
                continue

            shutil.rmtree(folder)

        except OSError:
            pass
