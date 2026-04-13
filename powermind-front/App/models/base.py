# app/models/base.py

from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


MesureValueType = int | float | bool
MesureKind = Literal['double', 'int', 'bool']
UserRole = Literal['admin', 'technicien', 'user']
AlerteCriticite = Literal['faible', 'moyenne', 'haute', 'critique']
AlerteStatut = Literal['active', 'resolue', 'ignoree']


class AppBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class TimestampedModel(AppBaseModel):
    created_at: datetime


class UUIDModel(AppBaseModel):
    id: UUID


class UUIDTimestampedModel(UUIDModel, TimestampedModel):
    pass


class PaginationParams(AppBaseModel):
    page: int = 1
    page_size: int = 20


class DateRangeFilter(AppBaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None