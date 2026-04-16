# app/models/mesure.py
from datetime import datetime
from uuid import UUID

from app.models.base import AppBaseModel, MesureValueType, UUIDTimestampedModel, UUIDModel


class MesureBase(AppBaseModel):
    capteur_id: UUID
    type_mesure_id: int  # int2 en BDD (1:CO2, 2:Humidité, 3:Température, 4:Présence)
    value: MesureValueType  # ATTENTION: colonne 'value' en BDD (pas 'valeur')


class Mesure(MesureBase, UUIDTimestampedModel):
    id: int  # int8 en BDD


class MesureCreate(MesureBase):
    pass


class MesureUpdate(AppBaseModel):
    value: MesureValueType | None = None


class MesureSummary(MesureBase, UUIDTimestampedModel):
    id: int


class MesureWithMeta(AppBaseModel):
    id: int  # int8 en BDD
    capteur_id: UUID
    capteur_nom: str
    type_mesure_id: int
    type_mesure_code: str
    unite: str | None = None
    value: MesureValueType  # colonne 'value' en BDD
    created_at: datetime
