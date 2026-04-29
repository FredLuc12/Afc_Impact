# app/services/installation_service.py

from uuid import UUID

from app.constants import TABLE_INSTALLATIONS
from app.models.installation import Installation, InstallationCreate, InstallationUpdate
from app.services.base_service import BaseService


class InstallationService(BaseService):
    table_name = TABLE_INSTALLATIONS

    def get_by_id(self, installation_id: UUID) -> Installation | None:
        response = self.table().select('*').eq('id', str(installation_id)).maybe_single().execute()
        data = self.extract_data(response)
        return Installation(**data) if data else None

    def list_all(self) -> list[Installation]:
        response = self.table().select('*').order('created_at', desc=True).execute()
        data = self.extract_data(response) or []
        return [Installation(**item) for item in data]

    def list_by_user(self, user_id: UUID) -> list[Installation]:
        print(user_id)
        response = (
            self.table()
            .select('*')
            .eq('user_id', str(user_id))
            .order('created_at', desc=True)
            .execute()
        )
        print(response.data)
        data = self.extract_data(response) or []
        return [Installation(**item) for item in data]

    def create(self, payload: InstallationCreate) -> Installation:
        response = self.table().insert(payload.model_dump()).execute()
        data = self.extract_data(response)[0]
        return Installation(**data)

    def update(self, installation_id: UUID, payload: InstallationUpdate) -> Installation:
        response = (
            self.table()
            .update(payload.model_dump(exclude_none=True))
            .eq('id', str(installation_id))
            .execute()
        )
        data = self.extract_data(response)[0]
        return Installation(**data)

    def delete(self, installation_id: UUID):
        return self.table().delete().eq('id', str(installation_id)).execute()