# app/state/filters_state.py

from datetime import datetime, timedelta
from uuid import UUID


class FiltersState:
    def __init__(self) -> None:
        self.installation_id: UUID | None = None
        self.capteur_id: UUID | None = None
        self.type_mesure_id: int | None = None   # int2 en BDD (pas UUID)
        self.search: str = ''
        self.start_date: datetime | None = datetime.now() - timedelta(days=7)
        self.end_date: datetime | None = datetime.now()
        # alert_status et alert_criticite supprimés : colonnes inexistantes en BDD

    def reset(self) -> None:
        self.installation_id = None
        self.capteur_id = None
        self.type_mesure_id = None
        self.search = ''
        self.start_date = datetime.now() - timedelta(days=7)
        self.end_date = datetime.now()

    def set_installation(self, installation_id: UUID | None) -> None:
        self.installation_id = installation_id

    def set_capteur(self, capteur_id: UUID | None) -> None:
        self.capteur_id = capteur_id

    def set_type_mesure(self, type_mesure_id: int | None) -> None:
        self.type_mesure_id = type_mesure_id

    def set_search(self, value: str) -> None:
        self.search = value.strip()

    def set_date_range(self, start_date: datetime | None, end_date: datetime | None) -> None:
        self.start_date = start_date
        self.end_date = end_date


filters_state = FiltersState()
