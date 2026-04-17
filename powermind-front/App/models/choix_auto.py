# app/models/choix_auto.py
# Structure BDD après migration :
# id (int8), installation_id (uuid FK), choix (text), created_at (timestamptz)
# Contrainte UNIQUE sur installation_id → UPSERT possible

from uuid import UUID
from datetime import datetime
from app.models.base import AppBaseModel


class ChoixAuto(AppBaseModel):
    id: int
    installation_id: UUID
    choix: str               # 'confort' | 'ecologique' | 'economique'
    created_at: datetime | None = None


class ChoixAutoCreate(AppBaseModel):
    installation_id: UUID
    choix: str


class ChoixAutoUpdate(AppBaseModel):
    choix: str | None = None


class ChoixAutoSummary(AppBaseModel):
    id: int
    installation_id: UUID
    choix: str
    created_at: datetime | None = None
