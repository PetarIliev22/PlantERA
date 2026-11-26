import json
import keyring

from config.version import APP_NAME
from keyring.errors import PasswordDeleteError

SERVICE_NAME = APP_NAME
SESSION_KEY = "supabase_session"

def save_session(access_token, refresh_token):
    session = {"access_token": access_token, "refresh_token": refresh_token}
    keyring.set_password(SERVICE_NAME, SESSION_KEY, json.dumps(session))
    
def load_session():
    session = keyring.get_password(SERVICE_NAME, SESSION_KEY)
    return json.loads(session) if session is not None else None

def clear_session():
    try:
        keyring.delete_password(SERVICE_NAME,SESSION_KEY)
    except PasswordDeleteError:
        if keyring.get_password(SERVICE_NAME, SESSION_KEY) is not None:
            raise