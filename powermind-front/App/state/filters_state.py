# app/state/filters_state.py

from datetime import datetime, timedelta
from uuid import UUID


class FiltersState:
    def __init__(self) -> None:
        self.installation_id: UUID | None = None
        self.capteur_id: UUID | None = None
        self.type_mesure_id: UUID | None = None
        self.search: str = ''
        self.alert_status: str | None = None
        self.alert_criticite: str | None = None
        self.start_date: datetime | None = datetime.now() - timedelta(days=7)
        self.end_date: datetime | None = datetime.now()

    def reset(self) -> None:
        self.installation_id = None
        self.capteur_id = None
        self.type_mesure_id = None
        self.search = ''
        self.alert_status = None
        self.alert_criticite = None
        self.start_date = datetime.now() - timedelta(days=7)
        self.end_date = datetime.now()

    def set_installation(self, installation_id: UUID | None) -> None:
        self.installation_id = installation_id

    def set_capteur(self, capteur_id: UUID | None) -> None:
        self.capteur_id = capteur_id

    def set_type_mesure(self, type_mesure_id: UUID | None) -> None:
        self.type_mesure_id = type_mesure_id

    def set_search(self, value: str) -> None:
        self.search = value.strip()

    def set_alert_status(self, value: str | None) -> None:
        self.alert_status = value

    def set_alert_criticite(self, value: str | None) -> None:
        self.alert_criticite = value

    def set_date_range(self, start_date: datetime | None, end_date: datetime | None) -> None:
        self.start_date = start_date
        self.end_date = end_date


filters_state = FiltersState()
