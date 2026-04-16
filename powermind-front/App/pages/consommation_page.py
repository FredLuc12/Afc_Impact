# app/pages/consommation_page.py
# Graphique historique des mesures sur 7 jours par type de capteur
# IDs BDD : 1=CO2, 2=Humidité, 3=Température, 4=Présence

from __future__ import annotations
from uuid import UUID
from datetime import datetime

from nicegui import ui

from app.core.notifications import notify_warning
from app.core.security import require_same_installation
from app.core.session import SessionManager
from app.core.utils import parse_uuid
from app.layouts.dashboard_layout import dashboard_layout
from app.services.mesure_service import MesureService
from app.services.choix_auto_service import ChoixAutoService

# Mapping type_mesure_id → label affichage
TYPES = {
    3: {'label': 'Température', 'unite': '°C',  'color': '#ef6670', 'icon': 'device_thermostat'},
    2: {'label': 'Humidité',    'unite': '%',   'color': '#5c67ec', 'icon': 'water_drop'},
    1: {'label': 'CO₂',        'unite': 'ppm', 'color': '#f59e0b', 'icon': 'co2'},
}


def _fmt_heure(iso: str) -> str:
    """Formate un timestamp ISO en heure lisible."""
    try:
        dt = datetime.fromisoformat(iso.replace('Z', '+00:00'))
        return dt.strftime('%d/%m %H:%M')
    except Exception:
        return iso[:10]


def consommation_page(installation_id: str | UUID | None = None) -> None:
    mesure_svc = MesureService()
    choix_svc  = ChoixAutoService()

    def content() -> None:
        current_installation_id = installation_id or SessionManager.get_installation_id()
        installation_uuid = parse_uuid(current_installation_id)

        if installation_uuid is None:
            notify_warning("Aucune installation valide n'est sélectionnée.")
            ui.label("Aucune installation sélectionnée.").classes('text-base font-semibold text-red-500')
            return

        if not require_same_installation(str(installation_uuid)):
            return

        # Dernier choix auto
        latest_choix = choix_svc.get_latest()
        mode_actif   = (latest_choix.choix if latest_choix else '—').upper()
        couleur_mode = '#5c67ec' if mode_actif == 'ELECTRIC' else '#f59e0b'

        ui.label('Historique des mesures sur 7 jours.').classes('text-[#9ca4ae] text-sm -mt-1')

        # --- KPI mode actif ---
        with ui.card().classes('w-full p-4 mb-1'):
            with ui.row().classes('items-center gap-3'):
                ui.icon('bolt', color='blue').classes('text-3xl')
                with ui.column().classes('gap-0'):
                    ui.label('Mode énergétique actif').classes('text-xs text-gray-400')
                    ui.label(mode_actif).style(f'font-size:1.3rem;font-weight:700;color:{couleur_mode}')

        # --- Sélecteur de type de mesure ---
        type_selectionne = {'id': 3}  # Température par défaut

        graphique_container = ui.column().classes('w-full')

        def afficher_graphique(type_id: int):
            graphique_container.clear()
            meta = TYPES.get(type_id, {'label': '?', 'unite': '', 'color': '#888', 'icon': 'sensors'})

            with graphique_container:
                historique = mesure_svc.list_historique_par_type(
                    installation_uuid, type_id, jours=7, limit=200
                )

                if not historique:
                    with ui.card().classes('w-full p-6 items-center'):
                        ui.icon('bar_chart', color='grey').classes('text-4xl')
                        ui.label('Aucune donnée sur les 7 derniers jours.').classes('text-sm text-gray-400')
                    return

                valeurs   = [h['value'] for h in historique if h['value'] is not None]
                etiquettes = [_fmt_heure(h['created_at']) for h in historique if h['value'] is not None]

                if not valeurs:
                    ui.label('Données insuffisantes.').classes('text-sm text-gray-400')
                    return

                val_min = min(valeurs)
                val_max = max(valeurs)
                val_moy = round(sum(valeurs) / len(valeurs), 1)

                # KPI min/moy/max
                with ui.row().classes('w-full gap-2 flex-wrap mb-2'):
                    for libelle, val in [('Min', val_min), ('Moy', val_moy), ('Max', val_max)]:
                        with ui.card().classes('p-3 flex-1 min-w-[80px] items-center'):
                            ui.label(libelle).classes('text-xs text-gray-400')
                            ui.label(f"{val} {meta['unite']}").classes('text-base font-bold text-slate-700')

                # Graphique ECharts
                with ui.card().classes('w-full p-3'):
                    # On ne prend que les 50 derniers points pour la lisibilité
                    pts   = valeurs[-50:]
                    lbls  = etiquettes[-50:]

                    echart = ui.echart({
                        'tooltip': {
                            'trigger': 'axis',
                            'formatter': f'{{b}}<br/>{{a}}: {{c}} {meta["unite"]}',
                        },
                        'grid': {'left': '8%', 'right': '4%', 'bottom': '18%', 'top': '8%'},
                        'xAxis': {
                            'type': 'category',
                            'data': lbls,
                            'axisLabel': {'rotate': 35, 'fontSize': 10},
                        },
                        'yAxis': {
                            'type': 'value',
                            'name': meta['unite'],
                            'nameTextStyle': {'fontSize': 10},
                        },
                        'series': [{
                            'name': meta['label'],
                            'type': 'line',
                            'data': pts,
                            'smooth': True,
                            'lineStyle': {'color': meta['color'], 'width': 2},
                            'itemStyle': {'color': meta['color']},
                            'areaStyle': {'color': meta['color'], 'opacity': 0.08},
                            'symbol': 'circle',
                            'symbolSize': 4,
                        }],
                    }).classes('w-full').style('height: 220px')

                ui.label(f"{len(valeurs)} mesure(s) sur 7 jours.").classes('text-[10px] text-gray-300 text-right w-full')

        # Boutons de sélection du type
        with ui.row().classes('w-full gap-2 mb-2 flex-wrap'):
            for tid, meta in TYPES.items():
                def make_handler(t=tid):
                    def handler():
                        type_selectionne['id'] = t
                        afficher_graphique(t)
                    return handler
                btn_color = 'blue-6' if tid == 3 else 'grey-5'
                ui.button(
                    meta['label'],
                    icon=meta['icon'],
                    on_click=make_handler()
                ).props(f'color={btn_color} outline').classes('text-xs')

        # Affichage initial
        afficher_graphique(type_selectionne['id'])

    dashboard_layout(title='Consommation', content=content, show_back=True)
