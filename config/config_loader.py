import json
# from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# @lru_cache(maxsize=32)
def load_config(filename):
    return json.loads(
        (BASE_DIR / filename).read_text(encoding="utf-8")
    )