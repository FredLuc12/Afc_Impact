# app/pages/dashboard_page.py
# CORRECTIONS BDD:
# - choix_auto: colonne 'choix' (pas 'mode'/'energie_choisie')
# - mesures: colonne 'value' (pas 'valeur')

from __future__ import annotations

from uuid import UUID

from nicegui import ui

from app.core.notifications import notify_error, notify_warning
from app.core.security import require_same_installation
from app.core.session import SessionManager
from app.core.utils import parse_uuid
from app.layouts.dashboard_layout import dashboard_layout
from app.services.dashboard_service import DashboardService


def dashboard_page(installation_id: str | UUID | None = None) -> None:
    service = DashboardService()

    def content() -> None:
        current_installation_id = installation_id or SessionManager.get_installation_id()
        installation_uuid = parse_uuid(current_installation_id)

        if installation_uuid is None:
            notify_warning("Aucune installation valide n'est sélectionnée.")
            ui.label('Aucune installation sélectionnée.').classes('text-base font-semibold text-red-500')
            ui.label("Impossible d'afficher le tableau de bord sans installation.").classes(
                'text-[#9ca4ae] text-sm -mt-1'
            )
            return

        if not require_same_installation(str(installation_uuid)):
            return

        try:
            data = service.get_installation_overview(installation_uuid)
        except Exception as e:
            notify_error(f'Erreur lors du chargement du dashboard : {str(e)}')
            ui.label('Impossible de charger les données du dashboard.').classes(
                'text-base font-semibold text-red-500'
            )
            return

        installation = data.get('installation') or {}
        capteurs = data.get('capteurs') or []
        mesures = data.get('mesures') or []
        alertes = data.get('alertes') or []
        # choix_auto: colonne 'choix' (pas 'mode' ni 'energie_choisie')
        latest_choix = data.get('latest_choix_auto') or {}

        ui.label(f"Installation : {installation.get('nom', '—')}").classes('text-base font-semibold')
        ui.label('Vue globale de supervision PowerMind.').classes('text-[#9ca4ae] text-sm -mt-1')

        with ui.row().classes('gap-3 wrap w-full'):
            with ui.card().classes('p-4 min-w-[180px]'):
                ui.label('Capteurs').classes('text-xs text-gray-500')
                ui.label(str(len(capteurs))).classes('text-2xl font-bold')

            with ui.card().classes('p-4 min-w-[180px]'):
                ui.label('Mesures récentes').classes('text-xs text-gray-500')
                ui.label(str(len(mesures))).classes('text-2xl font-bold')

            with ui.card().classes('p-4 min-w-[180px]'):
                ui.label('Alertes').classes('text-xs text-gray-500')
                ui.label(str(len(alertes))).classes('text-2xl font-bold')

            with ui.card().classes('p-4 min-w-[180px]'):
                ui.label('Dernier mode').classes('text-xs text-gray-500')
                # Colonne réelle en BDD: 'choix' (ex: 'electric', 'gaz')
                ui.label(str(latest_choix.get('choix', '—'))).classes('text-xl font-bold')

        ui.element('div').style('height: 12px')

        with ui.card().classes('w-full p-4'):
            ui.label('Dernier choix automatique').classes('text-sm font-semibold mb-2')
            if latest_choix:
                # Colonne 'choix' = mode énergétique sélectionné ('electric' ou 'gaz')
                ui.label(f"Énergie choisie : {latest_choix.get('choix', '—')}")
            else:
                ui.label('Aucun choix automatique disponible.').classes('text-sm text-gray-500')

        ui.element('div').style('height: 12px')

        with ui.card().classes('w-full p-4'):
            ui.label('Capteurs enregistrés').classes('text-sm font-semibold mb-2')
            if capteurs:
                for capteur in capteurs[:6]:
                    ui.label(f"- {capteur.get('nom', 'Capteur')} ({capteur.get('type', '—')})")
            else:
                ui.label('Aucun capteur trouvé.').classes('text-sm text-gray-500')

        ui.element('div').style('height: 12px')

        with ui.card().classes('w-full p-4'):
            ui.label('Dernières mesures').classes('text-sm font-semibold mb-2')
            if mesures:
                for mesure in mesures[:5]:
                    capteur_info = mesure.get('capteurs') or {}
                    type_info = mesure.get('types_mesure') or {}
                    # Colonne 'value' (pas 'valeur')
                    ui.label(
                        f"- {capteur_info.get('nom', '?')} | {type_info.get('code', '?')} : {mesure.get('value', '—')} {type_info.get('unite', '')}"
                    ).classes('text-sm')
            else:
                ui.label('Aucune mesure disponible.').classes('text-sm text-gray-500')

    dashboard_layout(title='Home', content=content, show_back=True)
