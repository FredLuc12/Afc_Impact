# app/services/consumption_service.py
# CORRECTIONS BDD:
# - mesures n'a PAS de colonne 'installation_id' → jointure via capteurs
# - colonne 'value' (pas 'valeur')
# - table 'energy_prices' n'existe PAS en BDD → supprimée
# - types_mesure (sans 's' final)

from __future__ import annotations

from uuid import UUID

from app.core.supabase_client import get_supabase_client


class ConsumptionService:
    def __init__(self) -> None:
        self.supabase = get_supabase_client()

    def get_consumption_overview(self, installation_id: UUID | str) -> dict:
        installation_id = str(installation_id)

        # Récupération des mesures via jointure capteurs (pas de installation_id direct sur mesures)
        # Colonne 'value' et table 'types_mesure' (noms réels BDD)
        mesures_response = (
            self.supabase.table('mesures')
            .select('id, value, created_at, capteur_id, type_mesure_id, capteurs!inner(installation_id), types_mesure(code, unite)')
            .eq('capteurs.installation_id', installation_id)
            .order('created_at', desc=True)
            .limit(50)
            .execute()
        )

        mesures = mesures_response.data or []

        current_percent = 0
        yesterday_percent = 0

        if mesures:
            # Utiliser la colonne 'value' (nom réel BDD)
            latest_values = [
                m.get('value', 0) for m in mesures[:10]
                if isinstance(m.get('value', 0), (int, float))
            ]
            previous_values = [
                m.get('value', 0) for m in mesures[10:20]
                if isinstance(m.get('value', 0), (int, float))
            ]

            if latest_values:
                current_percent = min(round(sum(latest_values) / len(latest_values)), 100)

            if previous_values:
                yesterday_percent = min(round(sum(previous_values) / len(previous_values)), 100)

        return {
            'current_percent': current_percent,
            'yesterday_percent': yesterday_percent,
            'market_prices': [],  # Table energy_prices absente de la BDD
            'measures': mesures,
        }
