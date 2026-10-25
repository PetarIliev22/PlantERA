import json
from unittest.mock import patch
from urllib.error import URLError

import pytest

from services.updates.update_service import check_for_updates, download_update


# ==================== HELPERS ====================

# Mock a GitHub release API response.
def mock_release_response(mock_urlopen, release):
    mock_urlopen.return_value.__enter__.return_value.read.return_value = (
        json.dumps(release).encode()
    )


# Mock a downloaded file response.
def mock_download_response(mock_urlopen, content):
    response = mock_urlopen.return_value.__enter__.return_value
    response.read.side_effect = [content, b""]
    response.headers = {"Content-Length": str(len(content))}


# ==================== UPDATE CHECKS ====================

# Verify that the current version does not trigger an update.
def test_no_update_when_version_is_current():
    release = {
        "tag_name": "v1.0.3",
        "assets": [
            {
                "name": "PlantERA.exe",
                "browser_download_url": "https://example.com/PlantERA.exe",
            }
        ],
    }

    with (
        patch("urllib.request.urlopen") as mock_urlopen,
        patch("services.updates.update_service.settings") as mock_settings,
    ):
        mock_settings.value.return_value = 0
        mock_release_response(mock_urlopen, release)

        result = check_for_updates()

        assert result is None
        mock_urlopen.assert_called_once()


# Verify that a newer release is detected correctly.
def test_update_available():
    release = {
        "tag_name": "v1.0.4",
        "body": "Bug fixes",
        "assets": [
            {
                "name": "PlantERA.exe",
                "browser_download_url": "https://example.com/PlantERA.exe",
            }
        ],
    }

    with (
        patch("urllib.request.urlopen") as mock_urlopen,
        patch("services.updates.update_service.settings") as mock_settings,
    ):
        mock_settings.value.return_value = 0
        mock_release_response(mock_urlopen, release)

        result = check_for_updates()

        assert result is not None
        assert result["version"] == "1.0.4"
        assert result["release_notes"] == "Bug fixes"
        mock_urlopen.assert_called_once()


# Verify that network errors do not crash the update check.
def test_update_check_handles_network_error():
    with (
        patch("urllib.request.urlopen", side_effect=URLError("No internet")),
        patch("services.updates.update_service.settings") as mock_settings,
    ):
        mock_settings.value.return_value = 0

        result = check_for_updates()

        assert result is None
        mock_settings.setValue.assert_not_called()


# ==================== UPDATE DOWNLOADS ====================

# Verify that files are downloaded successfully.
def test_download_success(tmp_path):
    content = b"PlantERA test update"

    asset = {
        "name": "PlantERA.exe",
        "browser_download_url": "https://example.com/PlantERA.exe",
    }

    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_download_response(mock_urlopen, content)

        progress = []

        result = download_update(
            asset,
            progress.append,
            download_dir=tmp_path,
        )

    assert result == tmp_path / "PlantERA.exe"
    assert result.read_bytes() == content
    assert progress[-1] == 100


# Verify that incomplete downloads are removed after network errors.
def test_download_cleans_up_on_network_error(tmp_path):
    asset = {
        "name": "PlantERA.exe",
        "browser_download_url": "https://example.com/PlantERA.exe",
    }

    with patch("urllib.request.urlopen", side_effect=URLError("Connection lost")):
        with pytest.raises(URLError):
            download_update(
                asset,
                download_dir=tmp_path,
            )

    assert not (tmp_path / "PlantERA.exe").exists()