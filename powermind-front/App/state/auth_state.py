# app/state/auth_state.py
# profiles en BDD : seulement id (uuid) + role (text) — pas d'email

from uuid import UUID
from app.models.profile import Profile


class AuthState:
    def __init__(self) -> None:
        self.is_authenticated: bool = False
        self.user_id: UUID | None = None
        self.profile: Profile | None = None
        self.email: str | None = None          # vient de Supabase Auth, pas de la table profiles
        self.access_token: str | None = None
        self.refresh_token: str | None = None

    @property
    def role(self) -> str | None:
        return self.profile.role if self.profile else None

    def login(
        self,
        user_id: UUID,
        profile: Profile | None = None,
        email: str | None = None,
        access_token: str | None = None,
        refresh_token: str | None = None,
    ) -> None:
        self.is_authenticated = True
        self.user_id = user_id
        self.profile = profile
        self.email = email
        self.access_token = access_token
        self.refresh_token = refresh_token

    def set_profile(self, profile: Profile) -> None:
        self.profile = profile
        self.user_id = profile.id

    def logout(self) -> None:
        self.is_authenticated = False
        self.user_id = None
        self.profile = None
        self.email = None
        self.access_token = None
        self.refresh_token = None


auth_state = AuthState()
