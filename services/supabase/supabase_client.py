import httpx
import threading
from supabase import Client, ClientOptions, create_client
from services.supabase.supabase_config import get_supabase_config
from services.supabase.supabase_session import save_session, clear_session, load_session

_client: Client | None = None
_lock = threading.Lock()

def handle_auth_state_change(event, session):
    if event in ("SIGNED_IN", "TOKEN_REFRESHED") and session is not None:
        if load_session() is not None:
            save_session(session.access_token, session.refresh_token)
        
    elif event == "SIGNED_OUT":
        clear_session()

def get_supabase_client() -> Client:
    global _client

    if _client is None:
        with _lock:
            if _client is None:
                url, key = get_supabase_config()
                http_client = httpx.Client()

                _client = create_client(
                    url,
                    key,
                    options=ClientOptions(
                        httpx_client=http_client
                    )
                )
                _client.auth.on_auth_state_change(handle_auth_state_change)
                
    return _client
    
