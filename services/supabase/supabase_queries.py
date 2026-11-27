import asyncio
from services.supabase.supabase_client import get_supabase_client

# Device models
def _fetch_device_models():
    client = get_supabase_client()
    response = (
        client.table("device_models")
        .select("*")
        .order("id")
        .execute()
    )
    return response.data

# User profile
def _fetch_user_profile(user_id):
    client = get_supabase_client()
    response = (
        client.table("profiles")
        .select("first_name, last_name, role, avatar, is_blocked")
        .eq("id", str(user_id))
        .single()
        .execute()
    )

    profile = response.data

    if profile["avatar"]:
        profile["avatar"] = bytes.fromhex(profile["avatar"][2:])

    return profile

# User avatar
def _update_user_avatar(user_id, image_data):
    client = get_supabase_client()

    client.table("profiles").update({
        "avatar": f"\\x{image_data.hex()}" if image_data else None
    }).eq("id", str(user_id)).execute()

# Async queries
async def get_device_models():
    return await asyncio.to_thread(_fetch_device_models)

async def get_user_profile(user_id):
    return await asyncio.to_thread(_fetch_user_profile, user_id)

async def update_user_avatar(user_id, image_data):
    return await asyncio.to_thread(
        _update_user_avatar, user_id, image_data
    )