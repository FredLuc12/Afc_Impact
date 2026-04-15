# app/core/utils.py

from __future__ import annotations

from datetime import datetime
from uuid import UUID


def safe_str(value: object | None, default: str = '—') -> str:
    if value is None:
        return default
    value = str(value).strip()
    return value if value else default


def parse_uuid(value: str | UUID | None) -> UUID | None:
    if not value:
        return None
    if isinstance(value, UUID):
        return value
    try:
        return UUID(str(value))
    except (ValueError, TypeError):
        return None


def format_datetime_fr(value: datetime | str | None) -> str:
    if not value:
        return '—'
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            return value
    return value.strftime('%d/%m/%Y %H:%M')


def is_admin_role(role: str | None) -> bool:
    return role in {'admin', 'super_admin'}


def is_technicien_role(role: str | None) -> bool:
    return role in {'admin', 'super_admin', 'technicien'}