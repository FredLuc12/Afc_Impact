# app/services/choix_auto_service.py

from uuid import UUID

from app.constants import TABLE_CHOIX_AUTO
from app.models.choix_auto import ChoixAuto, ChoixAutoCreate, ChoixAutoUpdate
from app.services.base_service import BaseService


class ChoixAutoService(BaseService):
    table_name = TABLE_CHOIX_AUTO

    def get_by_id(self, choix_auto_id: UUID) -> ChoixAuto | None:
        response = (
            self.table()
            .select('*')
            .eq('id', str(choix_auto_id))
            .maybe_single()
            .execute()
        )
        data = self.extract_data(response)
        return ChoixAuto(**data) if data else None

    def list_all(self, limit: int = 100) -> list[ChoixAuto]:
        response = (
            self.table()
            .select('*')
            .order('created_at', desc=True)
            .limit(limit)
            .execute()
        )
        data = self.extract_data(response) or []
        return [ChoixAuto(**item) for item in data]

    def list_by_installation(self, installation_id: UUID, limit: int = 100) -> list[ChoixAuto]:
        response = (
            self.table()
            .select('*')
            .eq('installation_id', str(installation_id))
            .order('created_at', desc=True)
            .limit(limit)
            .execute()
        )
        data = self.extract_data(response) or []
        return [ChoixAuto(**item) for item in data]

    def get_latest_by_installation(self, installation_id: UUID) -> ChoixAuto | None:
        response = (
            self.table()
            .select('*')
            .eq('installation_id', str(installation_id))
            .order('created_at', desc=True)
            .limit(1)
            .maybe_single()
            .execute()
        )
        data = self.extract_data(response)
        return ChoixAuto(**data) if data else None

    def create(self, payload: ChoixAutoCreate) -> ChoixAuto:
        response = self.table().insert(payload.model_dump()).execute()
        data = self.extract_data(response)[0]
        return ChoixAuto(**data)

    def update(self, choix_auto_id: UUID, payload: ChoixAutoUpdate) -> ChoixAuto:
        response = (
            self.table()
            .update(payload.model_dump(exclude_none=True))
            .eq('id', str(choix_auto_id))
            .execute()
        )
        data = self.extract_data(response)[0]
        return ChoixAuto(**data)

    def delete(self, choix_auto_id: UUID):
        return self.table().delete().eq('id', str(choix_auto_id)).execute()