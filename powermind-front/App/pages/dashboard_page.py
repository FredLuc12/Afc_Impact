# app/pages/dashboard_page.py
# Temps réel : ui.timer() recharge les mesures toutes les 30 secondes

from __future__ import annotations
from uuid import UUID

from nicegui import ui

from app.core.notifications import notify_error, notify_warning
from app.core.security import require_same_installation
from app.core.session import SessionManager
from app.core.utils import parse_uuid, format_datetime_fr
from app.layouts.dashboard_layout import dashboard_layout
from app.services.dashboard_service import DashboardService
from app.services.mesure_service import MesureService

# IDs types_mesure en BDD : 1=CO2, 2=Humidité, 3=Température, 4=Présence
TYPE_TEMP = 3
TYPE_HUM  = 2
TYPE_CO2  = 1


def dashboard_page(installation_id: str | UUID | None = None) -> None:
    service     = DashboardService()
    mesure_svc  = MesureService()

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

        installation  = data.get('installation') or {}
        capteurs      = data.get('capteurs') or []
        alertes       = data.get('alertes') or []
        latest_choix  = data.get('latest_choix_auto') or {}

        # --- En-tête ---
        ui.label(f"Installation : {installation.get('nom', '—')}").classes('text-base font-semibold')
        ui.label('Supervision en temps réel — PowerMind.').classes('text-[#9ca4ae] text-sm -mt-1')

        # --- KPI statiques ---
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
                choix_val = latest_choix.get('choix', '—').upper()
                couleur_e = 'text-blue-500' if choix_val == 'ELECTRIC' else 'text-orange-500'
                ui.label(choix_val).classes(f'text-xl font-bold {couleur_e}')

        ui.element('div').style('height: 4px')

        # --- Mesures temps réel (rafraîchissement toutes les 30s) ---
        ui.label('Dernières mesures').classes('text-sm font-semibold mt-2')

        mesures_container = ui.column().classes('w-full gap-2')

        # Conteneurs pour les valeurs live
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
                mesures = mesure_svc.list_by_installation(installation_uuid, limit=50)
                valeurs = {TYPE_TEMP: None, TYPE_HUM: None, TYPE_CO2: None}
                for m in mesures:
                    tid = m.get('type_mesure_id')
                    if tid in valeurs and valeurs[tid] is None:
                        unite = (m.get('types_mesure') or {}).get('unite', '')
                        valeurs[tid] = f"{m.get('value', '—')} {unite}".strip()

                temp_label.text = valeurs[TYPE_TEMP] or '—'
                hum_label.text  = valeurs[TYPE_HUM]  or '—'
                co2_label.text  = valeurs[TYPE_CO2]  or '—'
                derniere_maj.text = f"Mis à jour : {format_datetime_fr(None) or '—'}"
                from datetime import datetime
                derniere_maj.text = f"Mis à jour : {datetime.now().strftime('%H:%M:%S')}"
            except Exception:
                pass

        refresh_mesures()
        ui.timer(30.0, refresh_mesures)

        ui.element('div').style('height: 4px')

        # --- Historique des capteurs ---
        with ui.card().classes('w-full p-4'):
            ui.label('Capteurs enregistrés').classes('text-sm font-semibold mb-2')
            if capteurs:
                for capteur in capteurs[:8]:
                    with ui.row().classes('w-full items-center justify-between py-1 border-b border-gray-50 last:border-0'):
                        ui.label(capteur.get('nom', 'Capteur')).classes('text-sm')
                        ui.label(capteur.get('type', '—')).classes('text-xs text-gray-400')
            else:
                ui.label('Aucun capteur.').classes('text-sm text-gray-500')

        # --- Alertes récentes ---
        if alertes:
            ui.element('div').style('height: 4px')
            with ui.card().classes('w-full p-4 border-l-4 border-orange-400'):
                ui.label(f'{len(alertes)} alerte(s) active(s)').classes('text-sm font-semibold text-orange-600 mb-2')
                for alerte in alertes[:3]:
                    capteur_info = alerte.get('capteurs') or {}
                    ui.label(
                        f"• {capteur_info.get('nom', '?')} — {alerte.get('message', '—')}"
                    ).classes('text-xs text-slate-600')

    dashboard_layout(title='Dashboard', content=content, show_back=False)
