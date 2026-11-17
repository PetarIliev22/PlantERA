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

async def get_device_models():
    return await asyncio.to_thread(_fetch_device_models)
