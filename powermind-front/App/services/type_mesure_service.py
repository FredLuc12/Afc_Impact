# app/services/type_mesure_service.py
# id est int2 en BDD (pas UUID)

from app.constants import TABLE_TYPES_MESURES
from app.models.type_mesure import TypeMesure, TypeMesureCreate, TypeMesureUpdate
from app.services.base_service import BaseService


class TypeMesureService(BaseService):
    table_name = TABLE_TYPES_MESURES

    def get_by_id(self, type_mesure_id: int) -> TypeMesure | None:
        response = self.table().select('*').eq('id', type_mesure_id).maybe_single().execute()
        data = self.extract_data(response)
        return TypeMesure(**data) if data else None

    def get_by_code(self, code: str) -> TypeMesure | None:
        response = self.table().select('*').eq('code', code).maybe_single().execute()
        data = self.extract_data(response)
        return TypeMesure(**data) if data else None

    def list_all(self) -> list[TypeMesure]:
        response = self.table().select('*').order('id').execute()
        data = self.extract_data(response) or []
        return [TypeMesure(**item) for item in data]

    def create(self, payload: TypeMesureCreate) -> TypeMesure:
        response = self.table().insert(payload.model_dump()).execute()
        data = self.extract_data(response)[0]
        return TypeMesure(**data)

    def update(self, type_mesure_id: int, payload: TypeMesureUpdate) -> TypeMesure:
        response = (
            self.table()
            .update(payload.model_dump(exclude_none=True))
            .eq('id', type_mesure_id)
            .execute()
        )
        data = self.extract_data(response)[0]
        return TypeMesure(**data)

    def delete(self, type_mesure_id: int):
        return self.table().delete().eq('id', type_mesure_id).execute()
