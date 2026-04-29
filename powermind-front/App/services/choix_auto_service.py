# app/services/choix_auto_service.py
from uuid import UUID

from app.constants import TABLE_CHOIX_AUTO
from app.models.choix_auto import ChoixAuto, ChoixAutoCreate, ChoixAutoUpdate
from app.services.base_service import BaseService


class ChoixAutoService(BaseService):
    table_name = TABLE_CHOIX_AUTO

    def get_by_installation(self, installation_id: UUID) -> ChoixAuto | None:
        """
        Récupère le dernier choix enregistré pour une installation.
        On prend la ligne la plus récente (created_at desc, limit 1)
        car la table n'a pas de contrainte UNIQUE(installation_id) en BDD.
        """
        response = (
            self.table()
            .select('*')
            .eq('installation_id', str(installation_id))
            .order('created_at', desc=True)
            .limit(1)
            .execute()
        )
        data = self.extract_data(response)
        # extract_data retourne une liste avec limit(1)
        if not data:
            return None
        row = data[0] if isinstance(data, list) else data
        return ChoixAuto(**row)

    def upsert(self, installation_id: UUID, choix: str, **weights) -> ChoixAuto:
        """
        Insère un nouveau choix (insert simple, pas d'upsert car pas de
        contrainte UNIQUE en BDD). Les poids IA sont optionnels.
        """
        payload: dict = {
            'installation_id':    str(installation_id),
            'choix':              choix,
            'temp_importance':     weights.get('temp_importance'),
            'co2_importance':      weights.get('co2_importance'),
            'humidity_importance': weights.get('humidity_importance'),
            'pir_importance':      weights.get('pir_importance'),
        }
        # Nettoyer les None pour ne pas écraser des valeurs existantes
        payload = {k: v for k, v in payload.items() if v is not None or k in ('installation_id', 'choix')}

        response = self.table().insert(payload).execute()
        data = self.extract_data(response)
        row = data[0] if isinstance(data, list) else data
        return ChoixAuto(**row)

    def list_by_installation(self, installation_id: UUID, limit: int = 50) -> list[ChoixAuto]:
        """Historique des choix pour une installation, du plus récent au plus ancien."""
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