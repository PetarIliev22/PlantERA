import json
# from functools import lru_cache
from utils.paths import resource_path

# @lru_cache(maxsize=32)
def load_config(filename):
    path = resource_path("config", filename)

    return json.loads(
        path.read_text(encoding="utf-8")
    )