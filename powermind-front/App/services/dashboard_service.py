# app/services/dashboard_service.py
# CORRECTIONS BDD:
# - alertes: pas de installation_id direct → jointure via capteurs
# - choix_auto: pas de installation_id → on récupère le dernier enregistrement global
# - mesures: colonne 'value' (pas 'valeur'), jointure 'types_mesure' (pas 'types_mesures')

from uuid import UUID

from app.constants import (
    TABLE_ALERTES,
    TABLE_CAPTEURS,
    TABLE_CHOIX_AUTO,
    TABLE_INSTALLATIONS,
    TABLE_MESURES,
)
from app.services.base_service import BaseService


class DashboardService(BaseService):
    table_name = TABLE_INSTALLATIONS

    def get_installation_overview(self, installation_id: UUID, mesures_limit: int = 20) -> dict:
        mesures_limit = max(1, min(mesures_limit, 100))

        installation = self.extract_data(
            self.client.table(TABLE_INSTALLATIONS)
            .select('*')
            .eq('id', str(installation_id))
            .maybe_single()
            .execute()
        )

        capteurs = self.extract_data(
            self.client.table(TABLE_CAPTEURS)
            .select('*')
            .eq('installation_id', str(installation_id))
            .execute()
        ) or []

        # Jointure: 'types_mesure' (sans 's'), colonne 'value' (pas 'valeur')
        mesures = self.extract_data(
            self.client.table(TABLE_MESURES)
            .select('*, capteurs!inner(id, nom, installation_id), types_mesure(id, code, unite)')
            .eq('capteurs.installation_id', str(installation_id))
            .order('created_at', desc=True)
            .limit(mesures_limit)
            .execute()
        ) or []

        # alertes: pas de installation_id → jointure via capteurs
        alertes = self.extract_data(
            self.client.table(TABLE_ALERTES)
            .select('*, capteurs!inner(nom, installation_id)')
            .eq('capteurs.installation_id', str(installation_id))
            .order('created_at', desc=True)
            .limit(50)
            .execute()
        ) or []

        # choix_auto: pas de FK installation_id → on prend le dernier enregistrement global
        latest_choix = self.extract_data(
            self.client.table(TABLE_CHOIX_AUTO)
            .select('*')
            .order('id', desc=True)
            .limit(1)
            .maybe_single()
            .execute()
        )

        return {
            'installation': installation,
            'capteurs': capteurs,
            'mesures': mesures,
            'alertes': alertes,
            'latest_choix_auto': latest_choix,
        }

    def get_user_dashboard(self, user_id: UUID, mesures_limit_per_installation: int = 10) -> list[dict]:
        mesures_limit_per_installation = max(1, min(mesures_limit_per_installation, 50))

        installations = self.extract_data(
            self.client.table(TABLE_INSTALLATIONS)
            .select('*')
            .eq('user_id', str(user_id))
            .order('created_at', desc=True)
            .execute()
        ) or []

        # Dernier choix auto global (partagé, pas par installation)
        latest_choix = self.extract_data(
            self.client.table(TABLE_CHOIX_AUTO)
            .select('*')
            .order('id', desc=True)
            .limit(1)
            .maybe_single()
            .execute()
        )

        results: list[dict] = []

        for installation in installations:
            installation_id = installation.get('id')
            if not installation_id:
                continue

            capteurs = self.extract_data(
                self.client.table(TABLE_CAPTEURS)
                .select('*')
                .eq('installation_id', installation_id)
                .execute()
            ) or []

            # 'value' et 'types_mesure' (noms réels BDD)
            mesures = self.extract_data(
                self.client.table(TABLE_MESURES)
                .select('*, capteurs!inner(id, nom, installation_id), types_mesure(id, code, unite)')
                .eq('capteurs.installation_id', installation_id)
                .order('created_at', desc=True)
                .limit(mesures_limit_per_installation)
                .execute()
            ) or []

            # alertes via jointure capteurs (pas de installation_id direct)
            alertes = self.extract_data(
                self.client.table(TABLE_ALERTES)
                .select('*, capteurs!inner(nom, installation_id)')
                .eq('capteurs.installation_id', installation_id)
                .order('created_at', desc=True)
                .limit(20)
                .execute()
            ) or []

            results.append({
                'installation': installation,
                'capteurs': capteurs,
                'mesures': mesures,
                'latest_choix_auto': latest_choix,
                'alertes': alertes,
            })

        return results

    def get_latest_measurements_by_installation(self, installation_id: UUID, limit: int = 20) -> list[dict]:
        limit = max(1, min(limit, 100))
        response = (
            self.client.table(TABLE_MESURES)
            .select('*, capteurs!inner(id, nom, installation_id), types_mesure(id, code, unite)')
            .eq('capteurs.installation_id', str(installation_id))
            .order('created_at', desc=True)
            .limit(limit)
            .execute()
        )
        return self.extract_data(response) or []

    def get_alerts_by_installation(self, installation_id: UUID) -> list[dict]:
        """Alertes via jointure capteurs (alertes n'a pas de FK installation_id directe)."""
        response = (
            self.client.table(TABLE_ALERTES)
            .select('*, capteurs!inner(nom, installation_id)')
            .eq('capteurs.installation_id', str(installation_id))
            .order('created_at', desc=True)
            .limit(50)
            .execute()
        )
        return self.extract_data(response) or []

    def get_latest_choix_auto(self) -> dict | None:
        """Retourne le dernier choix auto global (pas de FK installation_id en BDD)."""
        response = (
            self.client.table(TABLE_CHOIX_AUTO)
            .select('*')
            .order('id', desc=True)
            .limit(1)
            .maybe_single()
            .execute()
        )
        return self.extract_data(response)
