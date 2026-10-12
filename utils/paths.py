import sys
from pathlib import Path


def resource_path(*parts):
    try:
        base_dir = Path(sys._MEIPASS)
    except Exception:
        base_dir = Path(__file__).resolve().parent.parent

    return base_dir.joinpath(*parts)