# app/models/type_mesure.py

from typing import Optional
from uuid import UUID

from app.models.base import AppBaseModel, MesureKind


class TypeMesure(AppBaseModel):
    id: UUID
    code: str
    unite: str | None = None
    kind: MesureKind


class TypeMesureCreate(AppBaseModel):
    code: str
    unite: str | None = None
    kind: MesureKind


class TypeMesureUpdate(AppBaseModel):
    code: Optional[str] = None
    unite: Optional[str] = None
    kind: Optional[MesureKind] = None


class TypeMesureSummary(AppBaseModel):
    id: UUID
    code: str
    unite: str | None = None
    kind: MesureKind