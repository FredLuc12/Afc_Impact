# app/services/api_client.py

from supabase import Client, create_client

from app.config import settings


class SupabaseClientManager:
    _client: Client | None = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._client is None:
            if not settings.supabase_url or not settings.supabase_anon_key:
                raise ValueError('SUPABASE_URL et SUPABASE_ANON_KEY sont requis')
            cls._client = create_client(settings.supabase_url, settings.supabase_anon_key)
        return cls._client


def get_supabase_client() -> Client:
    return SupabaseClientManager.get_client()