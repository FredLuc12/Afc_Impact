# app/pages/consommation_page.py
from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from uuid import UUID

from nicegui import ui

from app.core.notifications import notify_warning
from app.core.security import require_same_installation
from app.core.session import SessionManager
from app.core.utils import parse_uuid
from app.layouts.dashboard_layout import dashboard_layout
from app.services.mesure_service import MesureService


def _fmt_datetime(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y %H:%M')
    except Exception:
        return iso[:16] if iso else '—'


def consommation_page(installation_id: str | UUID | None = None) -> None:
    # MesureService.list_by_installation() fait la jointure :
    #   capteurs!inner(id, nom, installation_id) + types_mesure(id, code, unite)
    svc = MesureService()

    def content() -> None:
        current_installation_id = installation_id or SessionManager.get_installation_id()
        installation_uuid = parse_uuid(current_installation_id)

        if installation_uuid is None:
            notify_warning("Aucune installation valide n'est sélectionnée.")
            ui.label("Aucune installation sélectionnée.").classes('text-base font-semibold text-red-500')
            return

        if not require_same_installation(str(installation_uuid)):
            return

        # ─── Mesures avec nom du capteur ──────────────────────────────────
        # list_by_installation retourne des dicts avec clés :
        #   id, value, created_at, capteur_id, type_mesure_id,
        #   capteurs: {id, nom, installation_id},
        #   types_mesure: {id, code, unite}
        raw = svc.list_by_installation(installation_uuid, limit=100)

        if not raw:
            ui.label("Aucune donnée").classes("text-red-500")
            return

        # Aplatir pour le tableau
        all_mesures: list[dict] = []
        for m in raw:
            capteur     = m.get('capteurs')     or {}
            type_mesure = m.get('types_mesure') or {}
            all_mesures.append({
                "Capteur": capteur.get('nom', '—'),
                "Type":    type_mesure.get('code', '—'),
                "Valeur":  m.get('value'),
                "Unité":   type_mesure.get('unite', ''),
                "Date":    _fmt_datetime(m.get('created_at', '')),
            })

        # =========================
        # 📊 TABLEAU (infinite scroll)
        # =========================
        page_size     = 10
        current_index = 0
        loading       = False
        rows: list[dict] = []

        with ui.column().classes("w-full h-80 overflow-auto border rounded") as container:
            table = ui.table(
                columns=[
                    {"name": "Capteur", "label": "Capteur", "field": "Capteur"},
                    {"name": "Type",    "label": "Type",    "field": "Type"},
                    {"name": "Valeur",  "label": "Valeur",  "field": "Valeur"},
                    {"name": "Unité",   "label": "Unité",   "field": "Unité"},
                    {"name": "Date",    "label": "Date",    "field": "Date"},
                ],
                rows=rows,
            ).classes("w-full")

        def load_more():
            nonlocal current_index, loading
            if loading:
                return
            loading = True
            chunk = all_mesures[current_index:current_index + page_size]
            if not chunk:
                loading = False
                return
            rows.extend(chunk)
            current_index += page_size
            table.update_rows(rows)
            loading = False

        load_more()

        ui.timer(0.3, lambda: ui.run_javascript(f"""
        const el = document.querySelector('[data-id="{container.id}"]');
        if (!el) return;
        if (el.scrollTop + el.clientHeight >= el.scrollHeight - 10) {{
            window.dispatchEvent(new Event("load_more_event"));
        }}
        """))
        ui.on("load_more_event", load_more)

        # =========================
        # 📈 GRAPH (ECharts)
        # raw est trié desc → on inverse pour affichage chronologique
        # =========================
        series_data:  dict[str, list] = defaultdict(list)
        dates_by_type: dict[str, list] = defaultdict(list)

        for m in reversed(raw):
            type_mesure = m.get('types_mesure') or {}
            code  = type_mesure.get('code', 'unknown')
            value = m.get('value')
            date  = _fmt_datetime(m.get('created_at', ''))
            series_data[code].append(value)
            dates_by_type[code].append(date)

        first_code = next(iter(series_data), None)
        x_dates = dates_by_type[first_code] if first_code else []

        ui.echart({
            "title":   {"text": "Évolution des mesures"},
            "tooltip": {"trigger": "axis"},
            "legend":  {"data": list(series_data.keys())},
            "xAxis":   {"type": "category", "data": x_dates},
            "yAxis":   {"type": "value"},
            "series": [
                {"name": code, "type": "line", "smooth": True, "data": values}
                for code, values in series_data.items()
            ],
        }).classes("w-full h-96 mt-6")

        # =========================
        # 📋 STATS PAR TYPE
        # =========================
        ui.label("Statistiques").classes("text-lg font-bold mt-6 mb-2")

        stats_by_type: dict[str, dict] = {}
        for m in raw:
            type_mesure = m.get('types_mesure') or {}
            code  = type_mesure.get('code')
            unite = type_mesure.get('unite', '')
            value = m.get('value')
            if not code or value is None:
                continue
            if code not in stats_by_type:
                stats_by_type[code] = {'values': [], 'unite': unite}
            try:
                stats_by_type[code]['values'].append(float(value))
            except (TypeError, ValueError):
                pass

        with ui.row().classes("w-full gap-3 flex-wrap"):
            for code, s in stats_by_type.items():
                vals = s['values']
                if not vals:
                    continue
                with ui.card().classes("p-3 min-w-[140px]"):
                    ui.label(code).classes("font-semibold")
                    ui.label(f"Min : {round(min(vals), 1)} {s['unite']}").classes("text-xs text-gray-500")
                    ui.label(f"Max : {round(max(vals), 1)} {s['unite']}").classes("text-xs text-gray-500")
                    ui.label(f"Moy : {round(sum(vals)/len(vals), 1)} {s['unite']}").classes("text-xs text-gray-500")

    dashboard_layout(title="Mesures", content=content, show_back=True)