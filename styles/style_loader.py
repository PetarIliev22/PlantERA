from pathlib import Path

def load_styles():
    styles_dir = Path(__file__).parent

    files = [
        "main_window.qss",
        "toolbar.qss",
        "sidebar.qss",
        "provision.qss",
        "boot_dialog.qss",
    ]

    return "\n".join(
        (styles_dir / file).read_text(encoding="utf-8")
        for file in files
    )