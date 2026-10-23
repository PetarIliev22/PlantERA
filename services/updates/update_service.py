import time
import json

from pathlib import Path
from PySide6.QtCore import QSettings
from packaging.version import Version, InvalidVersion

from config.version import APP_VERSION, GITHUB_RELEASES_API

CHECK_INTERVAL = 60 * 60
settings = QSettings("PlantERA", "PlantERA")

def check_for_updates():
    import urllib.request
    
    last_update_check = settings.value("last_update_check", 0, type=float)
    
    now = time.time()
    
    if now - last_update_check < CHECK_INTERVAL:
        print("Update check skipped")
        return None

    try:
        request = urllib.request.Request(
            GITHUB_RELEASES_API,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "PlantERA-Updater"
            }
        )

        with urllib.request.urlopen(request, timeout=5) as response:
            release = json.load(response)
            
        settings.setValue("last_update_check", now)
        print(f"Latest version: {release['tag_name']}")
        
        latest_version = release["tag_name"].lstrip("v")

        if Version(latest_version) > Version(APP_VERSION):
            exe_asset = next(
                (
                    asset for asset in release.get("assets", [])
                    if asset["name"] == "PlantERA.exe"
                ),
                None
            )

            if exe_asset:
                return {
                    "version": latest_version,
                    "download_url": exe_asset["browser_download_url"],
                    "release_notes": release.get("body", ""),
                    "assets": release.get("assets", [])
                }

    except (
        OSError,
        ValueError,
        KeyError,
        InvalidVersion
    ) as error:
        print(f"Update check failed: {error}")

    return None


def download_update(download_url, expected_sha256, progress_callback=None):
    import hashlib
    import tempfile
    import urllib.request

    update_dir = Path(tempfile.mkdtemp(prefix="plantera_update_"))
    new_exe = update_dir / "PlantERA.exe"

    sha256 = hashlib.sha256()

    try:
        request = urllib.request.Request(
            download_url,
            headers={"User-Agent": "PlantERA-Updater"}
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            total_size = int(response.headers.get("Content-Length", 0))
            downloaded = 0

            with open(new_exe, "wb") as file:
                while chunk := response.read(1024 * 1024):
                    file.write(chunk)
                    sha256.update(chunk)
                    downloaded += len(chunk)

                    if progress_callback and total_size > 0:
                        progress = min(
                            100,
                            int(downloaded * 100 / total_size)
                        )
                        progress_callback(progress)

        if sha256.hexdigest().lower() != expected_sha256.lower():
            raise ValueError("SHA256 mismatch")

        return new_exe

    except Exception:
        new_exe.unlink(missing_ok=True)
        raise

def get_update_checksum(release):
    import urllib.request
    checksum_asset = next(
        (
            asset for asset in release.get("assets", [])
            if asset["name"] == "SHA256SUMS.txt"
        ),
        None
    )

    if checksum_asset is None:
        raise RuntimeError(
            "SHA256SUMS.txt not found in GitHub Release"
        )

    request = urllib.request.Request(
        checksum_asset["browser_download_url"],
        headers={"User-Agent": "PlantERA-Updater"}
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        checksum_text = response.read().decode("utf-8")

    for line in checksum_text.splitlines():
        parts = line.strip().split()

        if len(parts) == 2 and parts[1].lstrip("*") == "PlantERA.exe":
            checksum = parts[0].lower()

            if (
                len(checksum) == 64
                and all(c in "0123456789abcdef" for c in checksum)
            ):
                return checksum

    raise ValueError("Invalid SHA256 checksum")
