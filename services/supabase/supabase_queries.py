import asyncio
from services.supabase.supabase_client import get_supabase_client

def _decode_avatar(profile):
    if profile["avatar"]:
        profile["avatar"] = bytes.fromhex(profile["avatar"][2:])

    return profile

# Device models
def _fetch_device_models():
    return (
        get_supabase_client()
        .table("device_models")
        .select("*")
        .order("id")
        .execute()
        .data
    )

# User profile
def _fetch_user_profile(user_id):
    response = (
        get_supabase_client()
        .table("profiles")
        .select("first_name, last_name, role, avatar, is_blocked")
        .eq("id", str(user_id))
        .single()
        .execute()
    )

    return _decode_avatar(response.data)

# User avatar
def _update_user_avatar(user_id, image_data):
    get_supabase_client().table("profiles").update({
        "avatar": f"\\x{image_data.hex()}" if image_data else None
    }).eq("id", str(user_id)).execute()

# Users management
def _fetch_users():
    response = (
        get_supabase_client()
        .table("profiles")
        .select("id, first_name, last_name, email, role, avatar, is_blocked")
        .order("created_at")
        .execute()
    )

    return [_decode_avatar(user) for user in response.data]

def _manage_user(user_id, role, is_blocked):
    get_supabase_client().rpc("manage_user", {
        "p_user_id": str(user_id),
        "p_role": role,
        "p_is_blocked": is_blocked
    }).execute()

def _delete_user(user_id):
    get_supabase_client().rpc("delete_user", {
        "p_user_id": str(user_id)
    }).execute()

# Async queries
async def get_device_models():
    return await asyncio.to_thread(_fetch_device_models)

async def get_user_profile(user_id):
    return await asyncio.to_thread(_fetch_user_profile, user_id)

async def update_user_avatar(user_id, image_data):
    return await asyncio.to_thread(_update_user_avatar, user_id, image_data)

async def get_users():
    return await asyncio.to_thread(_fetch_users)

async def manage_user(user_id, role, is_blocked):
    return await asyncio.to_thread(_manage_user, user_id, role, is_blocked)

async def delete_user(user_id):
    return await asyncio.to_thread(_delete_user, user_id)