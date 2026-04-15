# app/services/choix_auto_service.py
# STRUCTURE BDD RÉELLE:
# choix_auto: id (int8 PK), choix (text)
# PAS de FK installation_id dans cette table

from app.constants import TABLE_CHOIX_AUTO
from app.models.choix_auto import ChoixAuto, ChoixAutoCreate, ChoixAutoUpdate
from app.services.base_service import BaseService


class ChoixAutoService(BaseService):
    table_name = TABLE_CHOIX_AUTO

    def get_by_id(self, choix_auto_id: int) -> ChoixAuto | None:
        # id est int8 en BDD
        response = (
            self.table()
            .select('*')
            .eq('id', choix_auto_id)
            .maybe_single()
            .execute()
        )
        data = self.extract_data(response)
        return ChoixAuto(**data) if data else None

    def list_all(self, limit: int = 100) -> list[ChoixAuto]:
        response = (
            self.table()
            .select('*')
            .order('id', desc=True)
            .limit(limit)
            .execute()
        )
        data = self.extract_data(response) or []
        return [ChoixAuto(**item) for item in data]

    def get_latest(self) -> ChoixAuto | None:
        """Retourne le dernier choix automatique enregistré."""
        response = (
            self.table()
            .select('*')
            .order('id', desc=True)
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

    def update(self, choix_auto_id: int, payload: ChoixAutoUpdate) -> ChoixAuto:
        response = (
            self.table()
            .update(payload.model_dump(exclude_none=True))
            .eq('id', choix_auto_id)
            .execute()
        )
        data = self.extract_data(response)[0]
        return ChoixAuto(**data)

    def delete(self, choix_auto_id: int):
        return self.table().delete().eq('id', choix_auto_id).execute()
