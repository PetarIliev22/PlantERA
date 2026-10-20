import sys
from pathlib import Path

def resource_path(*parts):
    try:
        base_dir = Path(sys._MEIPASS)
    except AttributeError:
        base_dir = Path(__file__).resolve().parent.parent

    return base_dir.joinpath(*parts)