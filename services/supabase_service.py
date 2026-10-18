
import os
import asyncio
import logging

from dotenv import load_dotenv
from supabase import create_client
from utils.paths import resource_path
from services import supabase_queries

logger = logging.getLogger(__name__)

class SupabaseService:
    def __init__(self):
        load_dotenv(resource_path(".env"))

        self.url = os.environ["SUPABASE_URL"]
        self.key = os.environ["SUPABASE_KEY"]
        self.client = None

    def connect(self):
        if self.client is None:
            self.client = create_client(self.url, self.key)

        return self.client

    async def get_device_models(self):
        try:
            return await asyncio.to_thread(
                self._execute,
                supabase_queries.get_device_models
            )

        except Exception:
            logger.exception("Failed to fetch device models.")
            raise
    
    def _execute(self, query):
        client = self.connect()
        return query(client)

supabase_service = SupabaseService()
