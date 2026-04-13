# app/services/base_service.py

from typing import Any

from app.services.api_client import get_supabase_client


class BaseService:
    table_name: str = ''

    def __init__(self) -> None:
        self.client = get_supabase_client()

    def table(self):
        if not self.table_name:
            raise ValueError('table_name doit être défini dans le service')
        return self.client.table(self.table_name)

    @staticmethod
    def extract_data(response: Any):
        return getattr(response, 'data', response)