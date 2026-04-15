# app/services/sensor_service.py

from uuid import UUID

from app.constants import TABLE_CAPTEURS
from app.models.capteur import Capteur, CapteurCreate, CapteurUpdate
from app.services.base_service import BaseService


class SensorService(BaseService):
    table_name = TABLE_CAPTEURS

    def get_by_id(self, capteur_id: UUID) -> Capteur | None:
        response = (
            self.table()
            .select('*')
            .eq('id', str(capteur_id))
            .maybe_single()
            .execute()
        )
        data = self.extract_data(response)
        return Capteur(**data) if data else None

    def list_all(self) -> list[Capteur]:
        response = (
            self.table()
            .select('*')
            .order('created_at', desc=True)
            .execute()
        )
        data = self.extract_data(response) or []
        return [Capteur(**item) for item in data]

    def list_by_installation(self, installation_id: UUID) -> list[Capteur]:
        response = (
            self.table()
            .select('*')
            .eq('installation_id', str(installation_id))
            .order('created_at', desc=True)
            .execute()
        )
        data = self.extract_data(response) or []
        return [Capteur(**item) for item in data]

    def create(self, payload: CapteurCreate) -> Capteur:
        response = self.table().insert(payload.model_dump()).execute()
        data = self.extract_data(response)[0]
        return Capteur(**data)

    def update(self, capteur_id: UUID, payload: CapteurUpdate) -> Capteur:
        response = (
            self.table()
            .update(payload.model_dump(exclude_none=True))
            .eq('id', str(capteur_id))
            .execute()
        )
        data = self.extract_data(response)[0]
        return Capteur(**data)

    def delete(self, capteur_id: UUID):
        return self.table().delete().eq('id', str(capteur_id)).execute()