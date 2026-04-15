# app/pages/installations_page.py

from nicegui import ui

from app.layouts.dashboard_layout import dashboard_layout
from app.services.installation_service import InstallationService


def installations_page(user_id) -> None:
    service = InstallationService()

    def content() -> None:
        installations = service.list_by_user(user_id)

        ui.label('Liste des installations PowerMind suivies.').classes('text-[#9ca4ae] text-sm -mt-1')

        with ui.card().classes('w-full p-4'):
            ui.label('Installations').classes('text-sm font-semibold mb-2')

            if installations:
                for installation in installations:
                    with ui.row().classes('w-full items-center justify-between py-2 border-b border-gray-200 last:border-b-0'):
                        ui.label(installation.nom)
                        ui.label(str(installation.created_at.date())).classes('text-xs text-gray-500')
            else:
                ui.label('Aucune installation trouvée.').classes('text-sm text-gray-500')

    dashboard_layout(title='Installations', content=content, show_back=True)