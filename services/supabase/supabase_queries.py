import asyncio
from pathlib import Path
from mimetypes import guess_type
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

# User avatar
def _upload_user_avatar(user_id, file_path):
    client = get_supabase_client()

    file = Path(file_path)
    avatar_path = f"{user_id}/avatar{file.suffix.lower()}"
    content_type = guess_type(file.name)[0]

    client.storage.from_("avatars").upload(
        path=avatar_path,
        file=file.read_bytes(),
        file_options={
            "content-type": content_type,
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

async def upload_user_avatar(user_id, file_path):
    return await asyncio.to_thread(
        _upload_user_avatar, user_id, file_path
    )

async def get_user_avatar(avatar_path):
    return await asyncio.to_thread(
        _fetch_user_avatar, avatar_path
    )