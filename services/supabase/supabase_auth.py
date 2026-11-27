import asyncio
from services.supabase.supabase_client import get_supabase_client
from services.supabase.supabase_session import load_session

def _sign_in(email, password):
    return get_supabase_client().auth.sign_in_with_password({
        "email": email,
        "password": password
    })

def _sign_up(email, password, first_name, last_name):
    return get_supabase_client().auth.sign_up({
        "email": email,
        "password": password,
        "options": {
            "data": {
                "first_name": first_name,
                "last_name": last_name
            }
        }
    })

def _sign_out():
    return get_supabase_client().auth.sign_out()

def _restore_session():
    session = load_session()

    return get_supabase_client().auth.set_session(
        session["access_token"], session["refresh_token"]
    ) if session is not None else None

async def sign_in(email, password):
    return await asyncio.to_thread(_sign_in, email, password)

async def sign_up(email, password, first_name="", last_name=""):
    return await asyncio.to_thread(
        _sign_up,
        email,
        password,
        first_name,
        last_name
    )

async def sign_out():
    return await asyncio.to_thread(_sign_out)

async def restore_session():
    return await asyncio.to_thread(_restore_session)

async def get_active_session():
    client = get_supabase_client()
    return await asyncio.to_thread(client.auth.get_session)