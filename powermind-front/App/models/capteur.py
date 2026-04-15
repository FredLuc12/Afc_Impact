# app/models/capteur.py

from uuid import UUID

from app.models.base import AppBaseModel, UUIDTimestampedModel, UUIDModel


class CapteurBase(AppBaseModel):
    installation_id: UUID
    type: str
    nom: str


class Capteur(CapteurBase, UUIDTimestampedModel):
    pass


class CapteurCreate(CapteurBase):
    pass


class CapteurUpdate(AppBaseModel):
    type: str | None = None
    nom: str | None = None


class CapteurSummary(CapteurBase, UUIDModel):
    pass