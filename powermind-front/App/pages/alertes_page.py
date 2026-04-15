# app/pages/alertes_page.py
# CORRECTIONS BDD:
# - alertes: seulement capteur_id + message (pas de 'titre', 'niveau', 'statut')
# - Le service retourne des dicts (avec jointure capteurs.nom)

from __future__ import annotations
from uuid import UUID
from nicegui import ui
from app.core.notifications import notify_warning
from app.core.security import require_same_installation
from app.core.session import SessionManager
from app.core.utils import parse_uuid
from app.layouts.dashboard_layout import dashboard_layout
from app.services.alerte_service import AlerteService


def alertes_page(installation_id: str | UUID | None = None) -> None:
    service = AlerteService()

    def content() -> None:
        current_installation_id = installation_id or SessionManager.get_installation_id()
        installation_uuid = parse_uuid(current_installation_id)

        if installation_uuid is None:
            notify_warning("Aucune installation valide n'est sélectionnée.")
            ui.label("Aucune installation sélectionnée.").classes("text-base font-semibold text-red-500")
            return

        if not require_same_installation(str(installation_uuid)):
            return

        # Alertes via jointure capteurs (alertes n'a pas de FK installation_id directe)
        alertes = service.list_by_installation(installation_uuid) or []

        ui.label("Surveillez les événements critiques détectés par vos capteurs.").classes(
            "text-[#9ca4ae] text-sm -mt-1"
        )

        if not alertes:
            with ui.card().classes("w-full p-4 items-center"):
                ui.icon('check_circle', color='positive').classes('text-4xl')
                ui.label("Aucune alerte détectée.").classes("text-sm font-semibold")
                ui.label("Tous vos capteurs fonctionnent normalement.").classes("text-sm text-gray-500")
        else:
            with ui.element("div").classes("w-full flex flex-col gap-3"):
                for alerte in alertes[:20]:
                    # Nom du capteur via la jointure 'capteurs'
                    capteur_info = alerte.get("capteurs", {})
                    source_name = (
                        capteur_info.get("nom")
                        if isinstance(capteur_info, dict)
                        else "Capteur inconnu"
                    )

                    with ui.card().classes("w-full border-l-4 border-orange-400 p-3 shadow-sm"):
                        with ui.row().classes("w-full justify-between items-center"):
                            ui.label("Anomalie détectée").classes("font-bold text-slate-700")
                            ui.badge("ALERTE").props("color=orange")

                        # Seul champ texte disponible en BDD: 'message'
                        ui.label(
                            alerte.get("message", "Une anomalie a été relevée sur le capteur.")
                        ).classes("text-sm text-slate-500 my-1")

                        with ui.row().classes("w-full items-center gap-2 text-[11px] text-slate-400"):
                            ui.icon('sensors', size='14px')
                            ui.label(f"Source : {source_name}")
                            ui.label("•")
                            ui.label(f"Détecté le : {alerte.get('created_at', '—')}")

        # Résumé simple (plus de filtrage par niveau puisqu'il n'existe pas en BDD)
        ui.label("Résumé").classes("text-lg font-bold mt-6 mb-2")
        with ui.card().classes("w-full p-4"):
            ui.label(f"Total alertes : {len(alertes)}").classes("text-sm font-semibold")

    dashboard_layout(title="Centre d'Alertes", content=content, show_back=True)
