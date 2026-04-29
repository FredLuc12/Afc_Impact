from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from uuid import UUID

from app.core.supabase_client import get_supabase_client


class ConsumptionService:
    def __init__(self) -> None:
        self.supabase = get_supabase_client()
        

    def get_last_measurements(self, installation_id: UUID | str, limit: int = 200) -> list[dict]:
        installation_id = str(installation_id)

        print("Client Supabase =", self.supabase)

        test = self.supabase.table('mesures').select('*').limit(1).execute()

        print("TEST DATA =", test.data)
        print("TEST ERROR =", getattr(test, 'error', None))
        response = self.supabase.table('mesures').select('*').limit(10).execute()
        print(response.data)

        response = (
            self.supabase.table('mesures')
            .select('''
                value,
                created_at,
                capteurs!inner(installation_id),
                types_mesure!inner(code, unite)
            ''')
            .eq('capteurs.installation_id', installation_id)
            .order('created_at', desc=True)
            .limit(limit)
            .execute()
        )

        if getattr(response, 'error', None):
            print('❌ Supabase error:', response.error)
            return []

        mesures = response.data or []
        print('✅ mesures brutes:', mesures)

        result = []

        for m in mesures:
            tm = m.get('types_mesure') or {}

            code = tm.get('code')
            unite = tm.get('unite', '')
            value = m.get('value')
            created_at = m.get('created_at', '')

            if code is None or value is None:
                continue

            result.append({
                'code': code,
                'unite': unite,
                'value': value,
                'created_at': created_at,
            })

        print(f'📊 {len(result)} mesures exploitables')
        return result

    def get_historique_par_type(self, installation_id: UUID | str, limit: int = 200) -> dict:
        installation_id = str(installation_id)

        response = (
            self.supabase.table('mesures')
            .select('''
                value,
                created_at,
                capteurs!inner(installation_id),
                types_mesure!inner(code, unite)
            ''')
            .eq('capteurs.installation_id', installation_id)
            .order('created_at', desc=False)
            .limit(limit)
            .execute()
        )

        if getattr(response, 'error', None):
            print('❌ Supabase historique error:', response.error)
            return {}

        mesures = response.data or []
        grouped: dict[str, list] = defaultdict(list)

        for m in mesures:
            tm = m.get('types_mesure') or {}

            code = tm.get('code')
            unite = tm.get('unite', '')
            val = m.get('value')
            date_raw = m.get('created_at', '')

            if not code or val is None:
                continue

            try:
                dt = datetime.fromisoformat(date_raw.replace('Z', '+00:00'))
                date_label = dt.strftime('%d/%m %H:%M')
            except Exception:
                date_label = date_raw[:16]

            grouped[code].append({
                'date': date_label,
                'value': val,
                'unite': unite,
            })

        return dict(grouped)

    def get_stats_par_type(self, historique: dict) -> dict:
        stats = {}

        for code, points in historique.items():
            values = [p['value'] for p in points if isinstance(p['value'], (int, float))]

            if not values:
                continue

            stats[code] = {
                'min': round(min(values), 1),
                'max': round(max(values), 1),
                'moy': round(sum(values) / len(values), 1),
                'unite': points[0]['unite'] if points else '',
                'nb': len(values),
            }

        return stats

    def get_derniere_valeur_par_type(self, installation_id: UUID | str) -> dict:
        installation_id = str(installation_id)

        response = (
            self.supabase.table('mesures')
            .select('''
                value,
                created_at,
                capteurs!inner(installation_id),
                types_mesure!inner(code, unite)
            ''')
            .eq('capteurs.installation_id', installation_id)
            .order('created_at', desc=True)
            .limit(50)
            .execute()
        )

        if getattr(response, 'error', None):
            print('❌ Supabase derniere_valeur error:', response.error)
            return {}

        mesures = response.data or []
        derniere: dict[str, dict] = {}

        for m in mesures:
            tm = m.get('types_mesure') or {}
            code = tm.get('code')

            if code and code not in derniere:
                derniere[code] = {
                    'value': m.get('value'),
                    'unite': tm.get('unite', ''),
                    'date': m.get('created_at', ''),
                }

        return derniere