
import json
import urllib.request
from packaging.version import Version, InvalidVersion

from config.version import APP_VERSION, GITHUB_RELEASES_API

def check_for_updates():
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
                    "release_notes": release.get("body", "")
                }

    except (
        OSError,
        ValueError,
        KeyError,
        InvalidVersion
    ) as error:
        print(f"Update check failed: {error}")

    return None
