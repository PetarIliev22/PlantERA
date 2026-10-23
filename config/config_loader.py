
import json
from utils.paths import resource_path

CONFIG_FOLDERS = {
    "sidebar.json": "ui_config",
    "boot_dialog.json": "ui_config",
    "update_dialog.json": "ui_config",
    "device_actions.json": "devices_config",
    "device_connection.json": "devices_config",
    "device_console.json": "devices_config",
    "device_images.json": "devices_config",
    "device_profiles.json": "devices_config",
}

def load_config(filename):
    folder = CONFIG_FOLDERS.get(filename)

    if folder:
        path = resource_path("config", folder, filename)
    else:
        path = resource_path("config", filename)

    return json.loads(
        path.read_text(encoding="utf-8")
    )
