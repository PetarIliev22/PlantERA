import threading
from supabase import Client, create_client
from services.supabase.supabase_config import get_supabase_config

_client: Client | None = None
_lock = threading.Lock()

def get_supabase_client() -> Client:
    global _client

    if _client is None:
        with _lock:
            if _client is None:
                url, key = get_supabase_config()
                _client = create_client(url, key)

    return _client
