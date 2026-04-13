# app/services/dashboard_service.py

from uuid import UUID

from app.services.alerte_service import AlerteService
from app.services.capteur_service import CapteurService
from app.services.installation_service import InstallationService
from app.services.mesure_service import MesureService


class DashboardService:
    def __init__(self) -> None:
        self.installation_service = InstallationService()
        self.capteur_service = CapteurService()
        self.mesure_service = MesureService()
        self.alerte_service = AlerteService()

    def get_dashboard_data(self, user_id: UUID) -> dict:
        installations = self.installation_service.list_by_user(user_id)

        if not installations:
            return {
                'installations': [],
                'selected_installation': None,
                'capteurs': [],
                'mesures': [],
                'alertes': [],
                'stats': {
                    'installations_count': 0,
                    'capteurs_count': 0,
                    'alertes_actives_count': 0,
                    'mesures_count': 0,
                },
            }

        selected_installation = installations[0]
        capteurs = self.capteur_service.list_by_installation(selected_installation.id)
        mesures = self.mesure_service.list_by_installation(selected_installation.id, limit=50)
        alertes = self.alerte_service.list_by_installation(selected_installation.id)

        return {
            'installations': installations,
            'selected_installation': selected_installation,
            'capteurs': capteurs,
            'mesures': mesures,
            'alertes': alertes,
            'stats': {
                'installations_count': len(installations),
                'capteurs_count': len(capteurs),
                'alertes_actives_count': len([a for a in alertes if a.statut == 'active']),
                'mesures_count': len(mesures),
            },
        }