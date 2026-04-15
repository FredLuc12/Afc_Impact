# app/pages/installations_page.py

from nicegui import ui

from app.core.security import require_auth
from app.core.session import SessionManager
from app.core.utils import parse_uuid
from app.layouts.dashboard_layout import dashboard_layout
from app.services.installation_service import InstallationService
from app.constants import ROUTE_DASHBOARD


def installations_page() -> None:
    service = InstallationService()

    def content() -> None:
        if not require_auth():
            return

        user_id = SessionManager.get_user_id()
        if not user_id:
            ui.label('Impossible de récupérer l\'utilisateur.').classes('text-red-500')
            return

        installations = service.list_by_user(parse_uuid(user_id)) or []

        ui.label('Liste des installations PowerMind suivies.').classes('text-[#9ca4ae] text-sm -mt-1')

        with ui.card().classes('w-full p-4'):
            ui.label('Mes installations').classes('text-sm font-semibold mb-2')

            if installations:
                for installation in installations:
                    with ui.row().classes('w-full items-center justify-between py-2 border-b border-gray-200 last:border-b-0'):
                        with ui.column().classes('gap-0'):
                            ui.label(installation.nom).classes('text-sm font-semibold')
                            ui.label(str(installation.created_at.date())).classes('text-xs text-gray-400')
                        ui.button(
                            'Voir dashboard',
                            on_click=lambda i=installation: ui.navigate.to(f'{ROUTE_DASHBOARD}/{i.id}')
                        ).props('flat').classes('text-xs text-blue-500')
            else:
                ui.label('Aucune installation trouvée pour votre compte.').classes('text-sm text-gray-500')

    dashboard_layout(title='Installations', content=content, show_back=True)
