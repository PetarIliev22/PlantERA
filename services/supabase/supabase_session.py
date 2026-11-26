import json
import keyring

from config.version import APP_NAME
from keyring.errors import PasswordDeleteError
from services.supabase.supabase_profile_cache import load_profile, clear_profile, save_profile
SERVICE_NAME = APP_NAME
SESSION_KEY = "supabase_session"

def save_session(access_token, refresh_token, profile=None):
    session = {"access_token": access_token, "refresh_token": refresh_token}
    keyring.set_password(SERVICE_NAME, SESSION_KEY, json.dumps(session))
    
    if profile is not None:
        save_profile(
            profile["user_id"],
            profile["first_name"],
            profile["last_name"],
            profile["email"],
            profile.get("avatar")
        )
    
def load_session():
    session = keyring.get_password(SERVICE_NAME, SESSION_KEY)
    return {
        **json.loads(session),
        "profile": load_profile()
    } if session is not None else None

def clear_session():
    try:
        keyring.delete_password(SERVICE_NAME, SESSION_KEY)
    except PasswordDeleteError:
        if keyring.get_password(SERVICE_NAME, SESSION_KEY) is not None:
            raise
        
    clear_profile()