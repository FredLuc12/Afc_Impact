# app/services/alerte_service.py

from uuid import UUID

from app.constants import TABLE_ALERTES
from app.models.alerte import Alerte, AlerteCreate, AlerteUpdate
from app.services.base_service import BaseService


class AlerteService(BaseService):
    table_name = TABLE_ALERTES

    def get_by_id(self, alerte_id: UUID) -> Alerte | None:
        response = self.table().select('*').eq('id', str(alerte_id)).maybe_single().execute()
        data = self.extract_data(response)
        return Alerte(**data) if data else None

    def list_all(self) -> list[Alerte]:
        response = self.table().select('*').order('created_at', desc=True).execute()
        data = self.extract_data(response) or []
        return [Alerte(**item) for item in data]

    def list_active(self) -> list[Alerte]:
        response = (
            self.table()
            .select('*')
            .eq('statut', 'active')
            .order('created_at', desc=True)
            .execute()
        )
        data = self.extract_data(response) or []
        return [Alerte(**item) for item in data]

    def list_by_installation(self, installation_id: UUID) -> list[Alerte]:
        response = (
            self.table()
            .select('*')
            .eq('installation_id', str(installation_id))
            .order('created_at', desc=True)
            .execute()
        )
        data = self.extract_data(response) or []
        return [Alerte(**item) for item in data]

    def list_by_capteur(self, capteur_id: UUID) -> list[Alerte]:
        response = (
            self.table()
            .select('*')
            .eq('capteur_id', str(capteur_id))
            .order('created_at', desc=True)
            .execute()
        )
        data = self.extract_data(response) or []
        return [Alerte(**item) for item in data]

    def create(self, payload: AlerteCreate) -> Alerte:
        response = self.table().insert(payload.model_dump()).execute()
        data = self.extract_data(response)[0]
        return Alerte(**data)

    def update(self, alerte_id: UUID, payload: AlerteUpdate) -> Alerte:
        response = (
            self.table()
            .update(payload.model_dump(exclude_none=True))
            .eq('id', str(alerte_id))
            .execute()
        )
        data = self.extract_data(response)[0]
        return Alerte(**data)

    def mark_resolved(self, alerte_id: UUID) -> Alerte:
        response = (
            self.table()
            .update({'statut': 'resolue'})
            .eq('id', str(alerte_id))
            .execute()
        )
        data = self.extract_data(response)[0]
        return Alerte(**data)

    def delete(self, alerte_id: UUID):
        return self.table().delete().eq('id', str(alerte_id)).execute()