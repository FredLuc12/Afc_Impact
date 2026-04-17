# app/pages/dashboard_page.py
# IDs types_mesure en BDD : 1=CO2, 2=Humidité, 3=Température, 4=Présence

from __future__ import annotations
from uuid import UUID

from nicegui import ui

from app.core.notifications import notify_error, notify_warning
from app.core.security import require_same_installation
from app.core.session import SessionManager
from app.core.utils import parse_uuid
from app.layouts.dashboard_layout import dashboard_layout
from app.services.dashboard_service import DashboardService
from app.services.mesure_service import MesureService

# IDs BDD types_mesure
TYPE_CO2  = 1
TYPE_HUM  = 2
TYPE_TEMP = 3


def dashboard_page(installation_id: str | UUID | None = None) -> None:
    service    = DashboardService()
    mesure_svc = MesureService()

    def content() -> None:
        current_installation_id = installation_id or SessionManager.get_installation_id()
        installation_uuid = parse_uuid(current_installation_id)

        if installation_uuid is None:
            notify_warning("Aucune installation valide n'est sélectionnée.")
            ui.label('Aucune installation sélectionnée.').classes('text-base font-semibold text-red-500')
            return

        if not require_same_installation(str(installation_uuid)):
            return

        try:
            data = service.get_installation_overview(installation_uuid)
        except Exception as e:
            notify_error(f'Erreur chargement dashboard : {str(e)}')
            ui.label('Impossible de charger les données.').classes('text-base font-semibold text-red-500')
            return

        installation = data.get('installation') or {}
        capteurs     = data.get('capteurs') or []
        alertes      = data.get('alertes') or []
        latest_choix = data.get('latest_choix_auto') or {}

        # --- En-tête ---
        ui.label(f"Installation : {installation.get('nom', '—')}").classes('text-base font-semibold')
        ui.label('Supervision en temps réel — PowerMind.').classes('text-[#9ca4ae] text-sm -mt-1')

        # --- KPIs ---
        with ui.row().classes('gap-3 flex-wrap w-full'):
            with ui.card().classes('p-4 flex-1 min-w-[130px]'):
                ui.label('Capteurs').classes('text-xs text-gray-400')
                ui.label(str(len(capteurs))).classes('text-2xl font-bold text-slate-700')

            with ui.card().classes('p-4 flex-1 min-w-[130px]'):
                ui.label('Alertes').classes('text-xs text-gray-400')
                nb_alertes = len(alertes)
                couleur = 'text-red-500' if nb_alertes else 'text-green-500'
                ui.label(str(nb_alertes)).classes(f'text-2xl font-bold {couleur}')

            with ui.card().classes('p-4 flex-1 min-w-[130px]'):
                ui.label('Énergie active').classes('text-xs text-gray-400')
                # latest_choix est un dict BDD après Option B
                choix_val = (latest_choix.get('choix') or '—').upper()
                couleur_e = 'text-blue-500' if choix_val in ('ELECTRIC', 'CONFORT', 'ECOLOGIQUE') else 'text-orange-500'
                ui.label(choix_val).classes(f'text-xl font-bold {couleur_e}')

        ui.element('div').style('height: 4px')

        # --- Mesures temps réel ---
        ui.label('Dernières mesures').classes('text-sm font-semibold mt-2')

        with ui.row().classes('w-full gap-2 flex-wrap'):
            with ui.card().classes('p-3 flex-1 min-w-[100px] items-center'):
                ui.icon('device_thermostat', color='red').classes('text-2xl')
                ui.label('Température').classes('text-xs text-gray-400')
                temp_label = ui.label('—').classes('text-xl font-bold text-slate-700')
            with ui.card().classes('p-3 flex-1 min-w-[100px] items-center'):
                ui.icon('water_drop', color='blue').classes('text-2xl')
                ui.label('Humidité').classes('text-xs text-gray-400')
                hum_label = ui.label('—').classes('text-xl font-bold text-slate-700')
            with ui.card().classes('p-3 flex-1 min-w-[100px] items-center'):
                ui.icon('co2', color='orange').classes('text-2xl')
                ui.label('CO₂').classes('text-xs text-gray-400')
                co2_label = ui.label('—').classes('text-xl font-bold text-slate-700')

        derniere_maj = ui.label('').classes('text-[10px] text-gray-300 text-right w-full')

        def refresh_mesures():
            try:
                # list_by_installation retourne des dicts avec :
                # - type_mesure_id (int) directement sur le dict racine
                # - types_mesure: {code, unite} pour l'unité
                mesures = mesure_svc.list_by_installation(installation_uuid, limit=50)

                valeurs: dict[int, str | None] = {TYPE_TEMP: None, TYPE_HUM: None, TYPE_CO2: None}

                for m in mesures:
                    # type_mesure_id est une colonne directe de mesures (int2)
                    tid = m.get('type_mesure_id')
                    if tid in valeurs and valeurs[tid] is None:
                        tm    = m.get('types_mesure') or {}
                        unite = tm.get('unite', '')
                        val   = m.get('value')
                        if val is not None:
                            valeurs[tid] = f"{val} {unite}".strip()

                temp_label.text = valeurs[TYPE_TEMP] or '—'
                hum_label.text  = valeurs[TYPE_HUM]  or '—'
                co2_label.text  = valeurs[TYPE_CO2]  or '—'

                from datetime import datetime
                derniere_maj.text = f"Mis à jour : {datetime.now().strftime('%H:%M:%S')}"
            except Exception as ex:
                print(f"[dashboard] refresh_mesures error: {ex}")

        refresh_mesures()
        ui.timer(30.0, refresh_mesures)

        ui.element('div').style('height: 4px')

        # --- Liste capteurs ---
        with ui.card().classes('w-full p-4'):
            ui.label('Capteurs enregistrés').classes('text-sm font-semibold mb-2')
            if capteurs:
                for capteur in capteurs[:8]:
                    with ui.row().classes('w-full items-center justify-between py-1 border-b border-gray-50 last:border-0'):
                        ui.label(capteur.get('nom', 'Capteur')).classes('text-sm')
                        ui.label(capteur.get('type', '—')).classes('text-xs text-gray-400')
            else:
                ui.label('Aucun capteur.').classes('text-sm text-gray-500')

        # --- Alertes ---
        if alertes:
            ui.element('div').style('height: 4px')
            with ui.card().classes('w-full p-4 border-l-4 border-orange-400'):
                ui.label(f'{len(alertes)} alerte(s)').classes('text-sm font-semibold text-orange-600 mb-2')
                for alerte in alertes[:3]:
                    cap_info = alerte.get('capteurs') or {}
                    ui.label(
                        f"• {cap_info.get('nom', '?')} — {alerte.get('message', '—')}"
                    ).classes('text-xs text-slate-600')

    dashboard_layout(title='Dashboard', content=content, show_back=False)
