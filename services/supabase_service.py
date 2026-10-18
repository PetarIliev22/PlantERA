import os
import logging

from dotenv import load_dotenv
from supabase import create_client, Client
from postgrest.exceptions import APIError

from utils.paths import resource_path

logger = logging.getLogger(__name__)

class SupabaseService:
    def __init__(self):
        load_dotenv(resource_path(".env"))

        URL = os.getenv("SUPABASE_URL")
        KEY = os.getenv("SUPABASE_KEY")

        if not URL or not KEY:
            raise ValueError(
                "Supabase URL or API key is missing."
            )

        try:
            self.client: Client = create_client(URL, KEY)

        except Exception:
            logger.exception(
                "Failed to initialize Supabase client."
            )
            raise

    # Fetches device models from Supabase
    def get_device_models(self):
        try:
            response = (
                self.client.table("device_models")
                .select("*")
                .order("id")
                .execute()
            )

            return response.data

        except APIError:
            logger.exception(
                "Failed to fetch device models from Supabase."
            )
            raise

        except Exception:
            logger.exception(
                "Unexpected error while fetching device models."
            )
            raise
    