# app/services/__init__.py

from app.services.alerte_service import AlerteService
from app.services.api_client import get_supabase_client
from app.services.capteur_service import CapteurService
from app.services.dashboard_service import DashboardService
from app.services.installation_service import InstallationService
from app.services.mesure_service import MesureService
from app.services.profile_service import ProfileService
from app.services.type_mesure_service import TypeMesureService

__all__ = [
    'AlerteService',
    'CapteurService',
    'DashboardService',
    'InstallationService',
    'MesureService',
    'ProfileService',
    'TypeMesureService',
    'get_supabase_client',
]