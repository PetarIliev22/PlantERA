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
        .select("first_name, last_name, role, avatar_url")
        .eq("id", str(user_id))
        .single()
        .execute()
    )

    return response.data

# Upload user avatar
def _upload_user_avatar(user_id, image_data):
    client = get_supabase_client()
    avatar_path = f"{user_id}/avatar.jpg"

    client.storage.from_("avatars").upload(
        path=avatar_path,
        file=image_data,
        file_options={
            "content-type": "image/jpeg",
            "upsert": "true"
        }
    )

    client.table("profiles").update({
        "avatar_url": avatar_path
    }).eq("id", str(user_id)).execute()

    return avatar_path

# Fetch user avatar
def _fetch_user_avatar(avatar_path):
    if not avatar_path:
        return None

    client = get_supabase_client()

    return client.storage.from_("avatars").download(avatar_path)

async def get_device_models():
    return await asyncio.to_thread(_fetch_device_models)

async def get_user_profile(user_id):
    return await asyncio.to_thread(_fetch_user_profile, user_id)

async def upload_user_avatar(user_id, image_data):
    return await asyncio.to_thread(
        _upload_user_avatar, user_id, image_data
    )

async def get_user_avatar(avatar_path):
    return await asyncio.to_thread(
        _fetch_user_avatar, avatar_path
    )