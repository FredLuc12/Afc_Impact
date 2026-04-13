# app/services/profile_service.py

from uuid import UUID

from app.constants import TABLE_PROFILES
from app.models.profile import Profile, ProfileCreate, ProfileUpdate
from app.services.base_service import BaseService


class ProfileService(BaseService):
    table_name = TABLE_PROFILES

    def get_by_id(self, profile_id: UUID) -> Profile | None:
        response = self.table().select('*').eq('id', str(profile_id)).maybe_single().execute()
        data = self.extract_data(response)
        return Profile(**data) if data else None

    def get_by_email(self, email: str) -> Profile | None:
        response = self.table().select('*').eq('email', email).maybe_single().execute()
        data = self.extract_data(response)
        return Profile(**data) if data else None

    def list_all(self) -> list[Profile]:
        response = self.table().select('*').order('created_at', desc=True).execute()
        data = self.extract_data(response) or []
        return [Profile(**item) for item in data]

    def create(self, payload: ProfileCreate) -> Profile:
        response = self.table().insert(payload.model_dump()).execute()
        data = self.extract_data(response)[0]
        return Profile(**data)

    def update(self, profile_id: UUID, payload: ProfileUpdate) -> Profile:
        response = (
            self.table()
            .update(payload.model_dump(exclude_none=True))
            .eq('id', str(profile_id))
            .execute()
        )
        data = self.extract_data(response)[0]
        return Profile(**data)