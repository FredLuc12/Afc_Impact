# app/models/installation.py

from datetime import datetime
from typing import Optional
from uuid import UUID

from app.models.base import AppBaseModel


class Installation(AppBaseModel):
    id: UUID
    user_id: UUID
    nom: str
    created_at: datetime


class InstallationCreate(AppBaseModel):
    user_id: UUID
    nom: str


class InstallationUpdate(AppBaseModel):
    nom: Optional[str] = None


class InstallationSummary(AppBaseModel):
    id: UUID
    user_id: UUID
    nom: str