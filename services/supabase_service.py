
import os
import asyncio
import logging
import threading

from dotenv import load_dotenv
from supabase import create_client

from utils.paths import resource_path
from services import supabase_queries

logger = logging.getLogger(__name__)

class SupabaseService:
    def __init__(self):
        env_path = resource_path(".env")

        load_dotenv(
            dotenv_path=env_path,
            override=True
        )

        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")

        if not self.url or not self.key:
            raise RuntimeError(
                "Supabase configuration missing. "
                f"Environment file found: {env_path.is_file()}"
            )

        self.client = None
        self._lock = threading.Lock()

    def connect(self):
        if self.client is None:
            self.client = create_client(self.url, self.key)

        return self.client

    def _execute(self, query):
        with self._lock:
            client = self.connect()
            return query(client)

    async def get_device_models(self):
        try:
            return await asyncio.to_thread(
                self._execute,
                supabase_queries.get_device_models
            )

        except Exception:
            logger.exception("Failed to fetch device models.")
            raise


supabase_service = SupabaseService()
