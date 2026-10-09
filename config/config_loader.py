import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def load_config(filename):
    return json.loads(
        (BASE_DIR / filename).read_text(encoding="utf-8")
    )