# app/models/profile.py

from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from app.models.base import AppBaseModel, UserRole, UUIDTimestampedModel, UUIDModel


class ProfileBase(AppBaseModel):
    email: EmailStr
    role: UserRole = 'user'


class Profile(ProfileBase, UUIDTimestampedModel):
    pass


class ProfileCreate(ProfileBase):
    id: UUID


class ProfileUpdate(AppBaseModel):
    email: EmailStr | None = None
    role: UserRole | None = None


class ProfileSummary(ProfileBase, UUIDModel):
    pass