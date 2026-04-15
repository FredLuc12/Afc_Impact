# app/services/mesure_service.py

from datetime import datetime, timedelta
from uuid import UUID

from app.constants import TABLE_MESURES
from app.models.mesure import Mesure, MesureCreate, MesureUpdate, MesureWithMeta
from app.services.base_service import BaseService


class MesureService(BaseService):
    table_name = TABLE_MESURES

    def get_by_id(self, mesure_id: int) -> Mesure | None:
        response = self.table().select('*').eq('id', mesure_id).maybe_single().execute()
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

    def list_by_type_mesure(self, type_mesure_id: int, limit: int = 100) -> list[Mesure]:
        response = (
            self.table()
            .select('*')
            .eq('type_mesure_id', type_mesure_id)
            .order('created_at', desc=True)
            .limit(limit)
            .execute()
        )
        data = self.extract_data(response) or []
        return [Mesure(**item) for item in data]

    def list_by_installation(self, installation_id: UUID, limit: int = 100) -> list[dict]:
        response = (
            self.table()
            .select('*, capteurs!inner(id, nom, installation_id), types_mesure(id, code, unite)')
            .eq('capteurs.installation_id', str(installation_id))
            .order('created_at', desc=True)
            .limit(limit)
            .execute()
        )
        return self.extract_data(response) or []

    def list_historique_par_type(
        self,
        installation_id: UUID,
        type_mesure_id: int,
        jours: int = 7,
        limit: int = 200,
    ) -> list[dict]:
        """
        Retourne l'historique d'un type de mesure sur N jours pour une installation.
        Utilisé pour construire les graphiques (consommation, dashboard temps réel).
        Retourne: [{'value': int, 'created_at': str, 'capteur_nom': str}, ...]
        """
        since = (datetime.utcnow() - timedelta(days=jours)).isoformat()
        response = (
            self.table()
            .select('value, created_at, capteurs!inner(nom, installation_id)')
            .eq('capteurs.installation_id', str(installation_id))
            .eq('type_mesure_id', type_mesure_id)
            .gte('created_at', since)
            .order('created_at', desc=False)
            .limit(limit)
            .execute()
        )
        raw = self.extract_data(response) or []
        return [
            {
                'value': item.get('value'),
                'created_at': item.get('created_at', ''),
                'capteur_nom': (item.get('capteurs') or {}).get('nom', ''),
            }
            for item in raw
        ]

    def list_with_meta(self, limit: int = 100) -> list[MesureWithMeta]:
        response = (
            self.table()
            .select('id, value, created_at, capteur_id, type_mesure_id, capteurs(nom), types_mesure(code, unite)')
            .order('created_at', desc=True)
            .limit(limit)
            .execute()
        )
        data = self.extract_data(response) or []
        results = []
        for item in data:
            capteur = item.get('capteurs') or {}
            type_mesure = item.get('types_mesure') or {}
            results.append(
                MesureWithMeta(
                    id=item['id'],
                    capteur_id=item['capteur_id'],
                    capteur_nom=capteur.get('nom', ''),
                    type_mesure_id=item['type_mesure_id'],
                    type_mesure_code=type_mesure.get('code', ''),
                    unite=type_mesure.get('unite'),
                    value=item['value'],
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

    def update(self, mesure_id: int, payload: MesureUpdate) -> Mesure:
        response = (
            self.table()
            .update(payload.model_dump(exclude_none=True))
            .eq('id', mesure_id)
            .execute()
        )
        data = self.extract_data(response)[0]
        return Mesure(**data)

    def delete(self, mesure_id: int):
        return self.table().delete().eq('id', mesure_id).execute()
