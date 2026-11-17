import asyncio
from services.supabase.supabase_client import get_supabase_client

def _sign_in(email, password):
    return get_supabase_client().auth.sign_in_with_password({
        "email": email,
        "password": password
    })


def _sign_up(email, password):
    return get_supabase_client().auth.sign_up({
        "email": email,
        "password": password
    })

def _sign_out():
    return get_supabase_client().auth.sign_out()


async def sign_in(email, password):
    return await asyncio.to_thread(_sign_in, email, password)


async def sign_up(email, password):
    return await asyncio.to_thread(_sign_up, email, password)


async def sign_out():
    return await asyncio.to_thread(_sign_out)