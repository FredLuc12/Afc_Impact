# app/models/mesure.py
from datetime import datetime
from uuid import UUID

from app.models.base import AppBaseModel, MesureValueType, UUIDTimestampedModel, UUIDModel


class MesureBase(AppBaseModel):
    capteur_id: UUID
    type_mesure_id: UUID
    valeur: MesureValueType


class Mesure(MesureBase, UUIDTimestampedModel):
    pass


class MesureCreate(MesureBase):
    pass


class MesureUpdate(AppBaseModel):
    valeur: MesureValueType | None = None


class MesureSummary(MesureBase, UUIDTimestampedModel):
    pass


class MesureWithMeta(AppBaseModel):
    id: UUID
    capteur_id: UUID
    capteur_nom: str
    type_mesure_id: UUID
    type_mesure_code: str
    unite: str | None = None
    valeur: MesureValueType
    created_at: datetime