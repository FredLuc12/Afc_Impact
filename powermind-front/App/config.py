# app/config.py

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from app.constants import (
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
    DEFAULT_LANGUAGE,
    DEFAULT_TIMEZONE,
)

load_dotenv()


def _to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


def _to_int(value: str | None, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv('APP_NAME', APP_NAME)
    app_version: str = os.getenv('APP_VERSION', APP_VERSION)
    app_description: str = os.getenv('APP_DESCRIPTION', APP_DESCRIPTION)

    host: str = os.getenv('HOST', '0.0.0.0')
    port: int = _to_int(os.getenv('PORT'), 8080)
    reload: bool = _to_bool(os.getenv('RELOAD'), True)
    dark: bool = _to_bool(os.getenv('DARK_MODE'), False)
    language: str = os.getenv('APP_LANGUAGE', DEFAULT_LANGUAGE)
    timezone: str = os.getenv('APP_TIMEZONE', DEFAULT_TIMEZONE)

    storage_secret: str = os.getenv('STORAGE_SECRET', 'change-me')
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')

    supabase_url: str = os.getenv('SUPABASE_URL', '')
    supabase_anon_key: str = os.getenv('SUPABASE_ANON_KEY', '')
    supabase_service_key: str = os.getenv('SUPABASE_SERVICE_KEY', '')

    api_base_url: str = os.getenv('API_BASE_URL', '')
    enable_mock_data: bool = _to_bool(os.getenv('ENABLE_MOCK_DATA'), True)

    app_title: str = os.getenv('APP_TITLE', APP_NAME)
    favicon: str = os.getenv('APP_FAVICON', '⚡')


settings = Settings()