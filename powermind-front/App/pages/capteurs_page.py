# app/pages/capteurs_page.py

from __future__ import annotations
from uuid import UUID

from nicegui import ui

from app.core.notifications import notify_warning
from app.core.security import require_same_installation
from app.core.session import SessionManager
from app.core.utils import parse_uuid
from app.layouts.dashboard_layout import dashboard_layout
# CORRECTION: import de CapteurService (pas SensorService qui est un doublon)
from app.services.capteur_service import CapteurService


def capteurs_page(installation_id: str | UUID | None = None) -> None:
    service = CapteurService()

    def content() -> None:
        current_installation_id = installation_id or SessionManager.get_installation_id()
        installation_uuid = parse_uuid(current_installation_id)

        if installation_uuid is None:
            notify_warning("Aucune installation valide n'est sélectionnée.")
            ui.label("Aucune installation sélectionnée.").classes("text-base font-semibold text-red-500")
            return

        if not require_same_installation(str(installation_uuid)):
            return

        capteurs = service.list_by_installation(installation_uuid) or []

        ui.label("État des capteurs connectés au logement.").classes("text-[#9ca4ae] text-sm -mt-1")

        with ui.card().classes("w-full p-4"):
            ui.label("Capteurs enregistrés").classes("text-sm font-semibold mb-2")
            if capteurs:
                for capteur in capteurs:
                    with ui.row().classes("w-full items-center justify-between py-2 border-b border-gray-100 last:border-b-0"):
                        with ui.column().classes('gap-0'):
                            ui.label(capteur.nom).classes("text-sm font-semibold")
                            ui.label(capteur.type).classes("text-xs text-gray-400")
                        ui.icon('sensors', color='positive').classes('text-lg')
            else:
                ui.label("Aucun capteur disponible pour cette installation.").classes("text-sm text-gray-500")

        ui.element("div").style("height: 12px")

        with ui.row().classes("gap-3"):
            ui.label(f"Total : {len(capteurs)} capteur(s)").classes("text-sm text-gray-500")

    dashboard_layout(title="Capteurs", content=content, show_back=True)
