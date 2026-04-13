# app/models/capteur.py

from datetime import datetime
from typing import Optional
from uuid import UUID

from app.models.base import AppBaseModel


class Capteur(AppBaseModel):
    id: UUID
    installation_id: UUID
    type: str
    nom: str
    created_at: datetime


class CapteurCreate(AppBaseModel):
    installation_id: UUID
    type: str
    nom: str


class CapteurUpdate(AppBaseModel):
    type: Optional[str] = None
    nom: Optional[str] = None


class CapteurSummary(AppBaseModel):
    id: UUID
    installation_id: UUID
    type: str
    nom: str