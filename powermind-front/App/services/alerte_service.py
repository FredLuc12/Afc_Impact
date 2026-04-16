# app/services/alerte_service.py
# STRUCTURE BDD RÉELLE:
# alertes: capteur_id (uuid FK -> capteurs.id), message (text)
# Pas de 'titre', 'niveau', 'statut', ni 'installation_id' direct

from uuid import UUID
from app.constants import TABLE_ALERTES
from app.models.alerte import Alerte, AlerteCreate, AlerteUpdate
from app.services.base_service import BaseService


class AlerteService(BaseService):
    table_name = TABLE_ALERTES

    def get_by_id(self, alerte_id: UUID) -> Alerte | None:
        # On récupère aussi le nom du capteur via jointure
        response = (
            self.table()
            .select('*, capteurs(nom)')
            .eq('id', str(alerte_id))
            .maybe_single()
            .execute()
        )
        data = self.extract_data(response)
        return Alerte(**data) if data else None

    def list_by_installation(self, installation_id: UUID) -> list[dict]:
        """
        Récupère les alertes de tous les capteurs appartenant à une installation.
        La jointure se fait via capteurs.installation_id (alertes n'a pas de FK installation_id directe).
        """
        response = (
            self.table()
            .select('*, capteurs!inner(nom, installation_id)')
            .eq('capteurs.installation_id', str(installation_id))
            .order('created_at', desc=True)
            .execute()
        )
        return self.extract_data(response) or []

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

    def create(self, payload: AlerteCreate) -> Alerte | None:
        response = self.table().insert(payload.model_dump()).execute()
        data = self.extract_data(response)
        return Alerte(**data[0]) if data else None

    def delete(self, alerte_id: UUID):
        return self.table().delete().eq('id', str(alerte_id)).execute()
