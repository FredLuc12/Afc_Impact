# app/models/choix_auto.py

from datetime import datetime
from uuid import UUID

from app.models.base import AppBaseModel, UUIDTimestampedModel


class ChoixAutoBase(AppBaseModel):
    installation_id: UUID
    mode: str
    energie_choisie: str
    score_pac: float | None = None
    score_gaz: float | None = None
    temperature_interieure: float | None = None
    temperature_exterieure: float | None = None
    humidite: float | None = None
    co2: float | None = None
    presence: bool | None = None
    raison: str | None = None


class ChoixAuto(ChoixAutoBase, UUIDTimestampedModel):
    pass


class ChoixAutoCreate(ChoixAutoBase):
    pass


class ChoixAutoUpdate(AppBaseModel):
    mode: str | None = None
    energie_choisie: str | None = None
    score_pac: float | None = None
    score_gaz: float | None = None
    temperature_interieure: float | None = None
    temperature_exterieure: float | None = None
    humidite: float | None = None
    co2: float | None = None
    presence: bool | None = None
    raison: str | None = None


class ChoixAutoSummary(AppBaseModel):
    id: UUID
    installation_id: UUID
    mode: str
    energie_choisie: str
    created_at: datetime