# app/models/type_mesure.py
# STRUCTURE BDD RÉELLE:
# types_mesure: id (int2 PK), code (text), unite (text)
# IDs connus: 1:CO2, 2:Humidité, 3:Température, 4:Présence

from app.models.base import AppBaseModel


class TypeMesureBase(AppBaseModel):
    code: str
    unite: str | None = None


class TypeMesure(TypeMesureBase):
    id: int  # int2 en BDD (pas UUID)


class TypeMesureCreate(TypeMesureBase):
    pass


class TypeMesureUpdate(AppBaseModel):
    code: str | None = None
    unite: str | None = None


class TypeMesureSummary(TypeMesureBase):
    id: int
