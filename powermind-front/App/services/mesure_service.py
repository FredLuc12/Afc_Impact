# app/services/mesure_service.py

from uuid import UUID

from app.constants import TABLE_MESURES
from app.models.mesure import Mesure, MesureCreate, MesureUpdate, MesureWithMeta
from app.services.base_service import BaseService


class MesureService(BaseService):
    table_name = TABLE_MESURES

    def get_by_id(self, mesure_id: UUID) -> Mesure | None:
        response = self.table().select('*').eq('id', str(mesure_id)).maybe_single().execute()
        data = self.extract_data(response)
        return Mesure(**data) if data else None

    def list_all(self, limit: int = 100) -> list[Mesure]:
        response = (
            self.table()
            .select('*')
            .order('created_at', desc=True)
            .limit(limit)
            .execute()
        )
        data = self.extract_data(response) or []
        return [Mesure(**item) for item in data]

    def list_by_capteur(self, capteur_id: UUID, limit: int = 100) -> list[Mesure]:
        response = (
            self.table()
            .select('*')
            .eq('capteur_id', str(capteur_id))
            .order('created_at', desc=True)
            .limit(limit)
            .execute()
        )
        data = self.extract_data(response) or []
        return [Mesure(**item) for item in data]

    def list_by_type_mesure(self, type_mesure_id: UUID, limit: int = 100) -> list[Mesure]:
        response = (
            self.table()
            .select('*')
            .eq('type_mesure_id', str(type_mesure_id))
            .order('created_at', desc=True)
            .limit(limit)
            .execute()
        )
        data = self.extract_data(response) or []
        return [Mesure(**item) for item in data]

    def list_by_installation(self, installation_id: UUID, limit: int = 100) -> list[dict]:
        response = (
            self.table()
            .select('*, capteurs!inner(id, nom, installation_id), types_mesures(id, code, unite, kind)')
            .eq('capteurs.installation_id', str(installation_id))
            .order('created_at', desc=True)
            .limit(limit)
            .execute()
        )
        return self.extract_data(response) or []

    def list_with_meta(self, limit: int = 100) -> list[MesureWithMeta]:
        response = (
            self.table()
            .select('id, valeur, created_at, capteur_id, type_mesure_id, capteurs(nom), types_mesures(code, unite)')
            .order('created_at', desc=True)
            .limit(limit)
            .execute()
        )
        data = self.extract_data(response) or []
        results = []
        for item in data:
            capteur = item.get('capteurs') or {}
            type_mesure = item.get('types_mesures') or {}
            results.append(
                MesureWithMeta(
                    id=item['id'],
                    capteur_id=item['capteur_id'],
                    capteur_nom=capteur.get('nom', ''),
                    type_mesure_id=item['type_mesure_id'],
                    type_mesure_code=type_mesure.get('code', ''),
                    unite=type_mesure.get('unite'),
                    valeur=item['valeur'],
                    created_at=item['created_at'],
                )
            )
        return results

    def create(self, payload: MesureCreate) -> Mesure:
        response = self.table().insert(payload.model_dump()).execute()
        data = self.extract_data(response)[0]
        return Mesure(**data)

    def create_many(self, payloads: list[MesureCreate]) -> list[Mesure]:
        response = self.table().insert([p.model_dump() for p in payloads]).execute()
        data = self.extract_data(response) or []
        return [Mesure(**item) for item in data]

    def update(self, mesure_id: UUID, payload: MesureUpdate) -> Mesure:
        response = (
            self.table()
            .update(payload.model_dump(exclude_none=True))
            .eq('id', str(mesure_id))
            .execute()
        )
        data = self.extract_data(response)[0]
        return Mesure(**data)

    def delete(self, mesure_id: UUID):
        return self.table().delete().eq('id', str(mesure_id)).execute()