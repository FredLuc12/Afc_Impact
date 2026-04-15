# app/services/consumption_service.py

from __future__ import annotations

from uuid import UUID

from app.core.supabase_client import get_supabase_client


class ConsumptionService:
    def __init__(self) -> None:
        self.supabase = get_supabase_client()

    def get_consumption_overview(self, installation_id: UUID | str) -> dict:
        installation_id = str(installation_id)

        mesures_response = (
            self.supabase.table('mesures')
            .select('id, type_mesure, valeur, created_at')
            .eq('installation_id', installation_id)
            .order('created_at', desc=True)
            .limit(50)
            .execute()
        )

        prix_response = (
            self.supabase.table('energy_prices')
            .select('energie, prix, devise, created_at')
            .order('created_at', desc=True)
            .limit(10)
            .execute()
        )

        mesures = mesures_response.data or []
        prix = prix_response.data or []

        current_percent = 0
        yesterday_percent = 0

        if mesures:
            latest_values = [m.get('valeur', 0) for m in mesures[:10] if isinstance(m.get('valeur', 0), (int, float))]
            previous_values = [m.get('valeur', 0) for m in mesures[10:20] if isinstance(m.get('valeur', 0), (int, float))]

            if latest_values:
                current_percent = min(round(sum(latest_values) / len(latest_values)), 100)

            if previous_values:
                yesterday_percent = min(round(sum(previous_values) / len(previous_values)), 100)

        market_prices = [
            {
                'name': item.get('energie', 'Énergie'),
                'price': f"{item.get('prix', '—')} {item.get('devise', '')}".strip(),
                'avatar': 'https://i.pravatar.cc/60?img=12',
            }
            for item in prix[:3]
        ]

        return {
            'current_percent': current_percent,
            'yesterday_percent': yesterday_percent,
            'market_prices': market_prices,
            'measures': mesures,
        }