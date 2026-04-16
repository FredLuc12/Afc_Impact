# app/core/session.py

from __future__ import annotations

from typing import Any

from nicegui import app


class SessionManager:
    @staticmethod
    def set_user_session(
        *,
        user_id: str,
        email: str,
        role: str,
        installation_id: str | None = None,
        profile_id: str | None = None,
        full_name: str | None = None,
    ) -> None:
        app.storage.user['authenticated'] = True
        app.storage.user['user_id'] = user_id
        app.storage.user['email'] = email
        app.storage.user['role'] = role
        app.storage.user['installation_id'] = installation_id
        app.storage.user['profile_id'] = profile_id
        app.storage.user['full_name'] = full_name

    @staticmethod
    def clear() -> None:
        app.storage.user.clear()

    @staticmethod
    def is_authenticated() -> bool:
        return bool(app.storage.user.get('authenticated', False))

    @staticmethod
    def get_user_id() -> str | None:
        return app.storage.user.get('user_id')

    @staticmethod
    def get_email() -> str | None:
        return app.storage.user.get('email')

    @staticmethod
    def get_role() -> str | None:
        return app.storage.user.get('role')

    @staticmethod
    def get_installation_id() -> str | None:
        return app.storage.user.get('installation_id')

    @staticmethod
    def get_profile_id() -> str | None:
        return app.storage.user.get('profile_id')

    @staticmethod
    def get_full_name() -> str | None:
        return app.storage.user.get('full_name')

    @staticmethod
    def get_all() -> dict[str, Any]:
        return dict(app.storage.user)

    @staticmethod
    def is_admin() -> bool:
        return app.storage.user.get('role') in ['admin', 'super_admin']