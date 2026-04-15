# app/pages/profil_page.py

from nicegui import ui

from app.core.notifications import notify_success, notify_error
from app.core.security import require_auth
from app.core.session import SessionManager
from app.layouts.dashboard_layout import dashboard_layout
from app.core.supabase_client import get_supabase_client


def profil_page() -> None:

    def content() -> None:
        if not require_auth():
            return

        # Données depuis la session
        full_name = SessionManager.get_full_name() or '—'
        email = SessionManager.get_email() or '—'
        role = SessionManager.get_role() or '—'
        user_id = SessionManager.get_user_id()
        installation_id = SessionManager.get_installation_id() or '—'

        ui.label('Informations de votre compte PowerMind.').classes('text-[#9ca4ae] text-sm -mt-1')

        # --- Infos lecture seule ---
        with ui.card().classes('w-full p-4 mb-3'):
            ui.label('Informations du compte').classes('text-sm font-semibold mb-3')

            with ui.row().classes('w-full justify-between items-center py-2 border-b border-gray-100'):
                ui.label('Nom complet').classes('text-xs text-gray-500')
                ui.label(full_name).classes('text-sm font-semibold')

            with ui.row().classes('w-full justify-between items-center py-2 border-b border-gray-100'):
                ui.label('Email').classes('text-xs text-gray-500')
                ui.label(email).classes('text-sm')

            with ui.row().classes('w-full justify-between items-center py-2 border-b border-gray-100'):
                ui.label('Rôle').classes('text-xs text-gray-500')
                ui.label(role.upper()).classes('text-sm font-semibold text-blue-600')

            with ui.row().classes('w-full justify-between items-center py-2'):
                ui.label('Installation ID').classes('text-xs text-gray-500')
                ui.label(str(installation_id)[:18] + '…' if len(str(installation_id)) > 18 else str(installation_id)).classes('text-xs text-gray-400 font-mono')

        # --- Modification du nom ---
        with ui.card().classes('w-full p-4'):
            ui.label('Modifier le nom affiché').classes('text-sm font-semibold mb-3')

            nom_input = ui.input('Nouveau nom', value=full_name).classes('w-full')

            def save_name():
                new_name = (nom_input.value or '').strip()
                if not new_name:
                    notify_error('Le nom ne peut pas être vide.')
                    return
                try:
                    supabase = get_supabase_client()
                    supabase.table('profiles').update({'full_name': new_name}).eq('id', user_id).execute()
                    app_storage = ui.context.client.storage
                    SessionManager.set_user_session(
                        user_id=user_id,
                        email=email,
                        role=role,
                        installation_id=installation_id,
                        full_name=new_name,
                    )
                    notify_success('Nom mis à jour avec succès.')
                except Exception as e:
                    notify_error(f'Erreur lors de la mise à jour : {str(e)}')

            ui.element('div').style('height: 8px')
            ui.button('Enregistrer', on_click=save_name).props('color=positive').classes('w-full')

        ui.element('div').style('height: 12px')

        # --- Déconnexion ---
        ui.button(
            'Se déconnecter',
            on_click=lambda: ui.navigate.to('/logout')
        ).props('color=negative flat').classes('w-full')

    dashboard_layout(title='Mon Profil', content=content, show_back=True)
