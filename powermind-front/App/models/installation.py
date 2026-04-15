# app/models/installation.py

from uuid import UUID

from app.models.base import AppBaseModel, UUIDTimestampedModel, UUIDModel


class InstallationBase(AppBaseModel):
    user_id: UUID
    nom: str


class Installation(InstallationBase, UUIDTimestampedModel):
    pass


class InstallationCreate(InstallationBase):
    pass


class InstallationUpdate(AppBaseModel):
    nom: str | None = None


class InstallationSummary(InstallationBase, UUIDModel):
    pass