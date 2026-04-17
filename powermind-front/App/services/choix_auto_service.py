# app/services/choix_auto_service.py
# Après migration : UPSERT par installation_id
# Une seule ligne active par installation — pas d'historique qui grossit

from uuid import UUID
from app.constants import TABLE_CHOIX_AUTO
from app.models.choix_auto import ChoixAuto, ChoixAutoCreate, ChoixAutoUpdate
from app.services.base_service import BaseService


class ChoixAutoService(BaseService):
    table_name = TABLE_CHOIX_AUTO

    def get_by_installation(self, installation_id: UUID) -> ChoixAuto | None:
        """Récupère le choix actif d'une installation."""
        response = (
            self.table()
            .select('*')
            .eq('installation_id', str(installation_id))
            .maybe_single()
            .execute()
        )
        data = self.extract_data(response)
        return ChoixAuto(**data) if data else None

    def upsert(self, installation_id: UUID, choix: str) -> ChoixAuto:
        """
        UPSERT : crée ou met à jour le choix pour cette installation.
        Grâce à la contrainte UNIQUE(installation_id), une seule ligne
        existe par installation — propre, pas d'accumulation.
        """
        response = (
            self.table()
            .upsert(
                {'installation_id': str(installation_id), 'choix': choix},
                on_conflict='installation_id',   # colonne contrainte UNIQUE
            )
            .execute()
        )
        data = self.extract_data(response)
        return ChoixAuto(**(data[0] if isinstance(data, list) else data))

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

    def delete(self, installation_id: UUID):
        return (
            self.table()
            .delete()
            .eq('installation_id', str(installation_id))
            .execute()
        )
