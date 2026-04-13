# app/models/alerte.py

from datetime import datetime
from typing import Optional
from uuid import UUID

from app.models.base import (
    AlerteCriticite,
    AlerteStatut,
    AppBaseModel,
)


class Alerte(AppBaseModel):
    id: UUID
    installation_id: UUID
    capteur_id: UUID | None = None
    type: str
    criticite: AlerteCriticite
    message: str
    statut: AlerteStatut
    created_at: datetime


class AlerteCreate(AppBaseModel):
    installation_id: UUID
    capteur_id: UUID | None = None
    type: str
    criticite: AlerteCriticite
    message: str
    statut: AlerteStatut = 'active'


class AlerteUpdate(AppBaseModel):
    type: Optional[str] = None
    criticite: Optional[AlerteCriticite] = None
    message: Optional[str] = None
    statut: Optional[AlerteStatut] = None


class AlerteSummary(AppBaseModel):
    id: UUID
    installation_id: UUID
    capteur_id: UUID | None = None
    type: str
    criticite: AlerteCriticite
    statut: AlerteStatut
    created_at: datetime