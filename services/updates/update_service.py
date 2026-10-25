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

def check_for_updates(force=False):
    import json
    import urllib.request
    from packaging.version import Version
    
    now = time.time()
    last_check = settings.value("last_update_check", 0, type=float)

    if not force and now - last_check < CHECK_INTERVAL:
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

def download_update(asset, progress_callback=None, download_dir=None):
    import tempfile
    import urllib.request
    from pathlib import Path

    path = Path(download_dir) if download_dir else Path(
        tempfile.mkdtemp(prefix="plantera_update_")
    )

    file_path = path / Path(asset["name"]).name

    try:
        with urllib.request.urlopen(
            create_request(asset["browser_download_url"]),
            timeout=30
        ) as response, file_path.open("wb") as file:

            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0

            while chunk := response.read(1024 * 1024):
                file.write(chunk)
                downloaded += len(chunk)

                if progress_callback and total:
                    progress_callback(
                        min(100, downloaded * 100 // total)
                    )

        return file_path

    except Exception:
        file_path.unlink(missing_ok=True)
        raise
