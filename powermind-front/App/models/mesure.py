# app/models/mesure.py

from datetime import datetime
from typing import Optional
from uuid import UUID

from app.models.base import AppBaseModel, MesureValueType


class Mesure(AppBaseModel):
    id: UUID
    capteur_id: UUID
    type_mesure_id: UUID
    valeur: MesureValueType
    created_at: datetime


class MesureCreate(AppBaseModel):
    capteur_id: UUID
    type_mesure_id: UUID
    valeur: MesureValueType


class MesureUpdate(AppBaseModel):
    valeur: Optional[MesureValueType] = None


class MesureSummary(AppBaseModel):
    id: UUID
    capteur_id: UUID
    type_mesure_id: UUID
    valeur: MesureValueType
    created_at: datetime


class MesureWithMeta(AppBaseModel):
    id: UUID
    capteur_id: UUID
    capteur_nom: str
    type_mesure_id: UUID
    type_mesure_code: str
    unite: str | None = None
    valeur: MesureValueType
    created_at: datetime