from pathlib import Path
from utils.paths import resource_path

def load_styles():
    styles_dir = resource_path("styles")

    files = [
        "main_window.qss",
        "toolbar.qss",
        "sidebar.qss",
        "boot_dialog.qss",
        "sidebar_profile.qss",
        "provision/device_connection.qss",
        "provision/device_info.qss",
        "provision/device_profile.qss",
        "provision/device_actions.qss",
        "provision/device_console.qss",
        "provision/provision_scroll.qss",
        "firmware/device_models.qss",
        "firmware/model_details.qss",
        "firmware/device_model_row.qss",
    ]

    styles = "\n".join(
        (styles_dir / file).read_text(encoding="utf-8")
        for file in files
    )
    assets_path = resource_path("assets", "img").as_posix()

    styles = styles.replace(
        "assets/img/",
        f"{assets_path}/"
    )

    return styles