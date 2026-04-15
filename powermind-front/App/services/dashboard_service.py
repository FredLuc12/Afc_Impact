# app/services/dashboard_service.py

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
        installation_response = (
            self.client.table(TABLE_INSTALLATIONS)
            .select('*')
            .eq('id', str(installation_id))
            .maybe_single()
            .execute()
        )
        installation = self.extract_data(installation_response)

        capteurs_response = (
            self.client.table(TABLE_CAPTEURS)
            .select('*')
            .eq('installation_id', str(installation_id))
            .order('created_at', desc=True)
            .execute()
        )
        capteurs = self.extract_data(capteurs_response) or []

        mesures_response = (
            self.client.table(TABLE_MESURES)
            .select('*, capteurs!inner(id, nom, installation_id), types_mesures(id, code, unite, kind)')
            .eq('capteurs.installation_id', str(installation_id))
            .order('created_at', desc=True)
            .limit(mesures_limit)
            .execute()
        )
        mesures = self.extract_data(mesures_response) or []

        alertes_response = (
            self.client.table(TABLE_ALERTES)
            .select('*')
            .eq('installation_id', str(installation_id))
            .order('created_at', desc=True)
            .execute()
        )
        alertes = self.extract_data(alertes_response) or []

        latest_choix_response = (
            self.client.table(TABLE_CHOIX_AUTO)
            .select('*')
            .eq('installation_id', str(installation_id))
            .order('created_at', desc=True)
            .limit(1)
            .maybe_single()
            .execute()
        )
        latest_choix = self.extract_data(latest_choix_response)

        return {
            'installation': installation,
            'capteurs': capteurs,
            'mesures': mesures,
            'alertes': alertes,
            'latest_choix_auto': latest_choix,
        }

    def get_user_dashboard(self, user_id: UUID, mesures_limit_per_installation: int = 10) -> list[dict]:
        installations_response = (
            self.client.table(TABLE_INSTALLATIONS)
            .select('*')
            .eq('user_id', str(user_id))
            .order('created_at', desc=True)
            .execute()
        )
        installations = self.extract_data(installations_response) or []

        results: list[dict] = []

        for installation in installations:
            installation_id = installation['id']

            capteurs_response = (
                self.client.table(TABLE_CAPTEURS)
                .select('*')
                .eq('installation_id', installation_id)
                .order('created_at', desc=True)
                .execute()
            )
            capteurs = self.extract_data(capteurs_response) or []

            mesures_response = (
                self.client.table(TABLE_MESURES)
                .select('*, capteurs!inner(id, nom, installation_id), types_mesures(id, code, unite, kind)')
                .eq('capteurs.installation_id', installation_id)
                .order('created_at', desc=True)
                .limit(mesures_limit_per_installation)
                .execute()
            )
            mesures = self.extract_data(mesures_response) or []

            latest_choix_response = (
                self.client.table(TABLE_CHOIX_AUTO)
                .select('*')
                .eq('installation_id', installation_id)
                .order('created_at', desc=True)
                .limit(1)
                .maybe_single()
                .execute()
            )
            latest_choix = self.extract_data(latest_choix_response)

            active_alertes_response = (
                self.client.table(TABLE_ALERTES)
                .select('*')
                .eq('installation_id', installation_id)
                .eq('statut', 'active')
                .order('created_at', desc=True)
                .execute()
            )
            active_alertes = self.extract_data(active_alertes_response) or []

            results.append(
                {
                    'installation': installation,
                    'capteurs': capteurs,
                    'mesures': mesures,
                    'latest_choix_auto': latest_choix,
                    'alertes_actives': active_alertes,
                }
            )

        return results

    def get_latest_measurements_by_installation(self, installation_id: UUID, limit: int = 20) -> list[dict]:
        response = (
            self.client.table(TABLE_MESURES)
            .select('*, capteurs!inner(id, nom, installation_id), types_mesures(id, code, unite, kind)')
            .eq('capteurs.installation_id', str(installation_id))
            .order('created_at', desc=True)
            .limit(limit)
            .execute()
        )
        return self.extract_data(response) or []

    def get_active_alerts_by_installation(self, installation_id: UUID) -> list[dict]:
        response = (
            self.client.table(TABLE_ALERTES)
            .select('*')
            .eq('installation_id', str(installation_id))
            .eq('statut', 'active')
            .order('created_at', desc=True)
            .execute()
        )
        return self.extract_data(response) or []

    def get_latest_choix_auto_by_installation(self, installation_id: UUID) -> dict | None:
        response = (
            self.client.table(TABLE_CHOIX_AUTO)
            .select('*')
            .eq('installation_id', str(installation_id))
            .order('created_at', desc=True)
            .limit(1)
            .maybe_single()
            .execute()
        )
        return self.extract_data(response)