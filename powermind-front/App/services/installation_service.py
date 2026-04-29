# app/services/installation_service.py
from uuid import UUID
from typing import Any

from app.constants import TABLE_INSTALLATIONS, TABLE_CAPTEURS
from app.models.installation import Installation, InstallationCreate, InstallationUpdate
from app.services.base_service import BaseService


class InstallationService(BaseService):
    table_name = TABLE_INSTALLATIONS

    def get_by_id(self, installation_id: UUID) -> Installation | None:
        response = (
            self.table()
            .select('*')
            .eq('id', str(installation_id))
            .limit(1)
            .execute()
        )
        data = self.extract_data(response)
        if not data:
            return None
        row = data[0] if isinstance(data, list) else data
        return Installation(**row)

    def list_all(self) -> list[Installation]:
        response = (
            self.table()
            .select('*')
            .order('created_at', desc=True)
            .execute()
        )
        data = self.extract_data(response) or []
        return [Installation(**item) for item in data]

    def list_all_with_details(self) -> list[dict[str, Any]]:
        """
        Retourne toutes les installations avec leurs capteurs imbriqués
        et le profil utilisateur associé.
        """
        response = (
            self.table()
            .select('*, capteurs(id, nom, type), profiles(id, email)')
            .order('created_at', desc=True)
            .execute()
        )
        return self.extract_data(response) or []

    def list_by_user(self, user_id: UUID) -> list[Installation]:
        response = (
            self.table()
            .select('*')
            .eq('user_id', str(user_id))
            .order('created_at', desc=True)
            .execute()
        )
        data = self.extract_data(response) or []
        return [Installation(**item) for item in data]

    def get_users_lookup(self) -> dict[str, str]:
        """Retourne {user_id: email} depuis la table profiles."""
        response = (
            self.client.table('profiles')
            .select('id, email')
            .order('email')
            .execute()
        )
        data = self.extract_data(response) or []
        return {r['id']: r['email'] for r in data}

    # def create(self, payload: InstallationCreate) -> Installation:
    #     response = self.table().insert(payload.model_dump()).execute()
    #     data = self.extract_data(response)
    #     row = data[0] if isinstance(data, list) else data
    #     return Installation(**row)

    # def update(self, installation_id: UUID, payload: InstallationUpdate) -> Installation:
    #     response = (
    #         self.table()
    #         .update(payload.model_dump(exclude_none=True))
    #         .eq('id', str(installation_id))
    #         .execute()
    #     )
    #     data = self.extract_data(response)
    #     row = data[0] if isinstance(data, list) else data
    #     return Installation(**row)
    
    def create(self, payload: InstallationCreate) -> Installation:
        # mode='json' convertit UUID → str, datetime → isoformat, etc.
        data = payload.model_dump(mode='json')
        response = self.table().insert(data).execute()
        row = self.extract_data(response)
        row = row[0] if isinstance(row, list) else row
        return Installation(**row)

    def update(self, installation_id: UUID, payload: InstallationUpdate) -> Installation:
        data = payload.model_dump(mode='json', exclude_none=True)
        response = (
            self.table()
            .update(data)
            .eq('id', str(installation_id))
            .execute()
        )
        row = self.extract_data(response)
        row = row[0] if isinstance(row, list) else row
        return Installation(**row)

    def delete(self, installation_id: UUID) -> None:
        self.table().delete().eq('id', str(installation_id)).execute()