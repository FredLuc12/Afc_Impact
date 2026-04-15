# app/models/alerte.py

from uuid import UUID
from datetime import datetime

from app.models.base import (
    AlerteCriticite,
    AlerteStatut,
    AppBaseModel,
    UUIDTimestampedModel,
)


class AlerteBase(AppBaseModel):
    installation_id: UUID
    capteur_id: UUID | None = None
    type: str
    criticite: AlerteCriticite
    message: str
    statut: AlerteStatut


class Alerte(AlerteBase, UUIDTimestampedModel):
    pass


class AlerteCreate(AppBaseModel):
    installation_id: UUID
    capteur_id: UUID | None = None
    type: str
    criticite: AlerteCriticite
    message: str
    statut: AlerteStatut = 'active'


class AlerteUpdate(AppBaseModel):
    type: str | None = None
    criticite: AlerteCriticite | None = None
    message: str | None = None
    statut: AlerteStatut | None = None


class AlerteSummary(AppBaseModel):
    id: UUID
    installation_id: UUID
    capteur_id: UUID | None = None
    type: str
    criticite: AlerteCriticite
    statut: AlerteStatut
    created_at: datetime