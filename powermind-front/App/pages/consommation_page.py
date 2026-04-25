from __future__ import annotations

from uuid import UUID
from datetime import datetime
from collections import defaultdict

from nicegui import ui

from app.core.notifications import notify_warning
from app.core.security import require_same_installation
from app.core.session import SessionManager
from app.core.utils import parse_uuid
from app.layouts.dashboard_layout import dashboard_layout
from app.core.supabase_client import get_supabase_client


def _fmt_datetime(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y %H:%M')
    except Exception:
        return iso[:16] if iso else '—'


def consommation_page(installation_id: str | UUID | None = None) -> None:
    supabase = get_supabase_client()

    def content() -> None:
        current_installation_id = installation_id or SessionManager.get_installation_id()
        installation_uuid = parse_uuid(current_installation_id)

        if installation_uuid is None:
            notify_warning("Aucune installation valide n'est sélectionnée.")
            ui.label("Aucune installation sélectionnée.").classes('text-base font-semibold text-red-500')
            return

        if not require_same_installation(str(installation_uuid)):
            return

        # 🔥 requête mesures
        response = (
            supabase
            .table("mesures")
            .select("""
                value,
                created_at,
                capteurs(nom),
                types_mesure(code, unite)
            """)
            .eq("capteurs.installation_id", str(installation_uuid))
            .order("created_at", desc=False)
            .limit(100)
            .execute()
        )

        mesures = response.data or []

        if not mesures:
            ui.label("Aucune donnée").classes("text-red-500")
            return

        # =========================
        # 📊 TABLEAU
        # =========================
        rows = []
        for m in mesures[:5]:
            print(m)
            rows.append({
                "Capteur": (m.get("capteurs") or {}).get("nom", "—"),
                "Type": (m.get("types_mesure") or {}).get("code", "—"),
                "Valeur": m.get("value"),
                "Unité": (m.get("types_mesure") or {}).get("unite", ""),
                "Date": _fmt_datetime(m.get("created_at", "")),
            })

        ui.table(
            columns=[
                {"name": "Capteur", "label": "Capteur", "field": "Capteur"},
                {"name": "Type", "label": "Type", "field": "Type"},
                {"name": "Valeur", "label": "Valeur", "field": "Valeur"},
                {"name": "Unité", "label": "Unité", "field": "Unité"},
                {"name": "Date", "label": "Date", "field": "Date"},
            ],
            rows=rows,
        ).classes("w-full")

        # =========================
        # 📈 GRAPH (ECharts)
        # =========================
        series = defaultdict(list)
        dates = []

        # tri chrono (important pour le graph)
        for m in reversed(mesures):
            dt = _fmt_datetime(m.get("created_at", ""))
            code = (m.get("types_mesure") or {}).get("code", "unknown")
            value = m.get("value")

            dates.append(dt)
            series[code].append(value)

        ui.echart({
            "title": {"text": "Évolution des mesures"},
            "tooltip": {"trigger": "axis"},
            "legend": {"data": list(series.keys())},
            "xAxis": {
                "type": "category",
                "data": dates
            },
            "yAxis": {
                "type": "value"
            },
            "series": [
                {
                    "name": key,
                    "type": "line",
                    "smooth": True,
                    "data": values
                }
                for key, values in series.items()
            ]
        }).classes("w-full h-96 mt-6")

    dashboard_layout(title="Mesures", content=content, show_back=True)