import asyncio
import httpx
from supabase import create_async_client, AsyncClientOptions
from services.supabase.supabase_config import get_supabase_config

class RealtimeService:
    def __init__(self):
        self.client = None
        self.http_client = None

    async def connect(self, access_token):
        if self.client is None:
            url, key = get_supabase_config()

            self.http_client = await asyncio.to_thread(httpx.AsyncClient)

            try:
                self.client = await create_async_client(
                    url,
                    key,
                    options=AsyncClientOptions(httpx_client=self.http_client)
                )
            except Exception:
                await self.http_client.aclose()
                self.http_client = None
                raise

        await self.update_token(access_token)

    async def subscribe(self, name, table, callback, event="*", row_filter=None):
        channel = self.client.channel(name)

        channel.on_postgres_changes(
            event,
            schema="public",
            table=table,
            filter=row_filter,
            callback=callback
        )

        await channel.subscribe()
        return channel

    async def unsubscribe(self, channel):
        await self.client.remove_channel(channel)

    async def update_token(self, access_token):
        if self.client is not None:
            await self.client.realtime.set_auth(access_token)

    async def disconnect(self):
        try:
            if self.client is not None:
                await self.client.realtime.close()

        finally:
            self.client = None

            if self.http_client is not None:
                await self.http_client.aclose()
                self.http_client = None