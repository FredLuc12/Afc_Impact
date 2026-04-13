# app/models/profile.py

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from app.models.base import AppBaseModel, UserRole


class Profile(AppBaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    created_at: datetime


class ProfileCreate(AppBaseModel):
    id: UUID
    email: EmailStr
    role: UserRole = 'user'


class ProfileUpdate(AppBaseModel):
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None


class ProfileSummary(AppBaseModel):
    id: UUID
    email: EmailStr
    role: UserRole