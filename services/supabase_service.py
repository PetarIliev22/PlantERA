
import os
import logging

from dotenv import load_dotenv
from supabase import acreate_client
from utils.paths import resource_path

logger = logging.getLogger(__name__)

class SupabaseService:
    def __init__(self):
        load_dotenv(resource_path(".env"))

        self.url = os.environ["SUPABASE_URL"]
        self.key = os.environ["SUPABASE_KEY"]
        self.client = None

    async def connect(self):
        if self.client is None:
            self.client = await acreate_client(self.url, self.key)

        return self.client

    # Get single model
    async def get_device_models(self):
        try:
            client = await self.connect()

            response = await (
                client.table("device_models")
                .select("*")
                .order("id")
                .execute()
            )

            return response.data

        except Exception:
            logger.exception("Failed to fetch device models.")
            raise


supabase_service = SupabaseService()
