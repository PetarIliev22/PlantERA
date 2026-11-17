import os
from dotenv import load_dotenv
from utils.paths import resource_path

def get_supabase_config():
    env_path = resource_path(".env")
    load_dotenv(dotenv_path=env_path, override=True)

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_PUBLISHABLE_KEY")

    if not url or not key:
        raise RuntimeError(
            "Supabase configuration missing. "
            f"Environment file found: {env_path.is_file()}"
        )

    return url, key