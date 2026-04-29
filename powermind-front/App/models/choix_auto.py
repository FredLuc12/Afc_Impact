# app/models/choix_auto.py
from uuid import UUID
from datetime import datetime
from app.models.base import AppBaseModel


class ChoixAuto(AppBaseModel):
    id: int
    installation_id: UUID
    choix: str
    temp_importance:     float | None = None
    co2_importance:      float | None = None
    humidity_importance: float | None = None
    pir_importance:      float | None = None
    created_at: datetime | None = None


class ChoixAutoCreate(AppBaseModel):
    installation_id: UUID
    choix: str
    temp_importance:     float | None = None
    co2_importance:      float | None = None
    humidity_importance: float | None = None
    pir_importance:      float | None = None


class ChoixAutoUpdate(AppBaseModel):
    choix:               str   | None = None
    temp_importance:     float | None = None
    co2_importance:      float | None = None
    humidity_importance: float | None = None
    pir_importance:      float | None = None


class ChoixAutoSummary(AppBaseModel):
    id: int
    installation_id: UUID
    choix: str
    created_at: datetime | None = None