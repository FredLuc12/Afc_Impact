from __future__ import annotations

from uuid import UUID

from nicegui import ui

from app.core.notifications import notify_warning
from app.core.security import require_same_installation
from app.core.session import SessionManager
from app.core.utils import parse_uuid
from app.layouts.dashboard_layout import dashboard_layout
from app.services.consumption_service import ConsumptionService


def consommation_page(installation_id: str | UUID | None = None) -> None:
    service = ConsumptionService()

    def content() -> None:
        current_installation_id = installation_id or SessionManager.get_installation_id()
        installation_uuid = parse_uuid(current_installation_id)

        if installation_uuid is None:
            notify_warning("Aucune installation valide n'est sélectionnée.")
            ui.label("Aucune installation sélectionnée.").classes("text-base font-semibold text-red-500")
            return

        if not require_same_installation(str(installation_uuid)):
            return

        data = service.get_consumption_overview(installation_uuid)

        ui.add_head_html(
            """
            <style>
                .pm-screen {
                    background: #f5f5f5;
                    min-height: 100vh;
                    padding: 20px 18px 28px 18px;
                    font-family: Inter, Arial, sans-serif;
                }
                .pm-back {
                    color: #ec6b73;
                    font-size: 24px;
                    font-weight: 500;
                    line-height: 1;
                    text-decoration: none;
                }
                .pm-title {
                    color: #3e4852;
                    font-size: 21px;
                    font-weight: 700;
                    margin-top: 18px;
                    margin-bottom: 24px;
                }
            </style>
            """
        )

        with ui.column().classes("pm-screen w-full").style("max-width: 390px; margin: 0 auto;"):
            ui.link("←", "/home").classes("pm-back")
            ui.label("Consommation").classes("pm-title")

            ui.label(f"Consommation actuelle : {data.get('current_percent', '—')}%")
            ui.label(f"Consommation hier : {data.get('yesterday_percent', '—')}%")

            ui.element("div").style("height: 12px")
            ui.label("Optimisations des profils").style("color:#3e4852;font-size:14px;font-weight:700;")

            ui.element("div").style("height: 12px")
            ui.label("Tarifs du marché").style("color:#3e4852;font-size:14px;font-weight:700;")

    dashboard_layout(title="Consommation", content=content, show_back=True)