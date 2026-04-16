# app/services/sensor_service.py

from uuid import UUID
from typing import Any

from app.constants import TABLE_CAPTEURS, TABLE_INSTALLATIONS
from app.models.capteur import Capteur, CapteurCreate, CapteurUpdate
from app.services.base_service import BaseService


class CapteurService(BaseService):
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

    # --- AJOUTS POUR L'INTERFACE ADMIN (EF14) ---

    def list_all_with_details(self) -> list[dict[str, Any]]:
        """Récupère tous les capteurs avec le nom de l'installation (via self.table())"""
        response = (
            self.table()
            .select('*, installations(id, nom)')
            .order('created_at', desc=True)
            .execute()
        )
        return self.extract_data(response) or []

    def get_installations_lookup(self) -> list[dict[str, Any]]:
        """Récupère la liste des installations via self.client"""
        response = (
            self.client.table(TABLE_INSTALLATIONS)
            .select('id, nom')
            .order('nom')
            .execute()
        )
        return self.extract_data(response) or []

    def toggle_activation(self, capteur_id: UUID, is_active: bool) -> bool:
        """Active ou désactive un capteur via self.table()"""
        try:
            self.table().update({'is_active': is_active}).eq('id', str(capteur_id)).execute()
            return True
        except Exception:
            return False