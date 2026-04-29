# app/models/profile.py
# BDD réelle : id (uuid), email (text), role (text), created_at (timestamptz)

from uuid import UUID
from datetime import datetime
from app.models.base import AppBaseModel, UserRole


class Profile(AppBaseModel):
    id: UUID
    email: str | None = None
    role: UserRole = 'user'
    created_at: datetime | None = None


class ProfileCreate(AppBaseModel):
    id: UUID
    email: str | None = None
    role: UserRole = 'user'


class ProfileUpdate(AppBaseModel):
    email: str | None = None
    role: UserRole | None = None


class ProfileSummary(AppBaseModel):
    id: UUID
    email: str | None = None
    role: UserRole
