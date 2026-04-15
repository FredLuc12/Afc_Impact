# app/models/type_mesure.py

from app.models.base import AppBaseModel, MesureKind, UUIDModel


class TypeMesureBase(AppBaseModel):
    code: str
    unite: str | None = None
    kind: MesureKind


class TypeMesure(TypeMesureBase, UUIDModel):
    pass


class TypeMesureCreate(TypeMesureBase):
    pass


class TypeMesureUpdate(AppBaseModel):
    code: str | None = None
    unite: str | None = None
    kind: MesureKind | None = None


class TypeMesureSummary(TypeMesureBase, UUIDModel):
    pass