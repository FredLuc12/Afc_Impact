# app/services/consumption_service.py

from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timezone
from uuid import UUID

from app.core.supabase_client import get_supabase_client


class ConsumptionService:
    def __init__(self) -> None:
        self.supabase = get_supabase_client()

    def get_historique_par_type(self, installation_id: UUID | str, limit: int = 200) -> dict:
        """
        Retourne l'historique des mesures groupé par type (code),
        trié par date croissante pour l'affichage en graphique.
        Structure retournée :
        {
            'TEMP_INT': [{'date': '...', 'value': 21}, ...],
            'TEMP_EXT': [...],
            'CO2':      [...],
            'HUM':      [...],
        }
        """
        installation_id = str(installation_id)

        response = (
            self.supabase.table('mesures')
            .select('value, created_at, types_mesure(code, unite), capteurs!inner(installation_id)')
            .eq('capteurs.installation_id', installation_id)
            .order('created_at', desc=False)
            .limit(limit)
            .execute()
        )

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

            # Format date court pour l'axe X
            try:
                dt = datetime.fromisoformat(date_raw.replace('Z', '+00:00'))
                date_label = dt.strftime('%d/%m %H:%M')
            exce
