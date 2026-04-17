# app/state/dashboard_state.py
# alertes en BDD : seulement capteur_id + message — pas de champ 'statut'

from app.models.capteur import Capteur
from app.models.installation import Installation
from app.models.mesure import MesureWithMeta


class DashboardState:
    def __init__(self) -> None:
        self.installations: list[Installation] = []
        self.selected_installation: Installation | None = None
        self.capteurs: list[Capteur] = []
        self.mesures: list[MesureWithMeta] = []
        self.alertes: list[dict] = []   # dicts bruts BDD (capteur_id, message)
        self.stats: dict = {
            'installations_count': 0,
            'capteurs_count': 0,
            'alertes_count': 0,
            'mesures_count': 0,
        }
        self.is_loading: bool = False
        self.error: str | None = None

    def reset(self) -> None:
        self.installations = []
        self.selected_installation = None
        self.capteurs = []
        self.mesures = []
        self.alertes = []
        self.stats = {
            'installations_count': 0,
            'capteurs_count': 0,
            'alertes_count': 0,
            'mesures_count': 0,
        }
        self.is_loading = False
        self.error = None

    def set_loading(self, value: bool) -> None:
        self.is_loading = value

    def set_error(self, message: str | None) -> None:
        self.error = message
        self.is_loading = False

    def set_data(self, payload: dict) -> None:
        self.installations = payload.get('installations', [])
        self.selected_installation = payload.get('selected_installation')
        self.capteurs = payload.get('capteurs', [])
        self.mesures = payload.get('mesures', [])
        self.alertes = payload.get('alertes', [])
        self.stats = payload.get('stats', self.stats)
        self.is_loading = False
        self.error = None

    @property
    def alertes_count(self) -> int:
        """Toutes les alertes sont actives en BDD (pas de champ statut)."""
        return len(self.alertes)

    @property
    def has_data(self) -> bool:
        return bool(self.installations or self.capteurs or self.mesures or self.alertes)


dashboard_state = DashboardState()
