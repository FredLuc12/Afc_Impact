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

        full_name       = SessionManager.get_full_name() or '—'
        email           = SessionManager.get_email() or '—'
        role            = SessionManager.get_role() or '—'
        user_id         = SessionManager.get_user_id()
        installation_id = SessionManager.get_installation_id() or '—'

        ui.label('Informations de votre compte PowerMind.').classes('text-[#9ca4ae] text-sm -mt-1')

        # --- Infos du compte ---
        with ui.card().classes('w-full p-4 mb-3'):
            ui.label('Mon compte').classes('text-sm font-semibold mb-3')

            for libelle, valeur, style in [
                ('Nom complet',     full_name,       'text-sm font-semibold'),
                ('Email',           email,           'text-sm'),
                ('Rôle',            role.upper(),    'text-sm font-semibold text-blue-600'),
                ('Installation ID', str(installation_id)[:22] + '…'
                                    if len(str(installation_id)) > 22
                                    else str(installation_id), 'text-xs text-gray-400 font-mono'),
            ]:
                with ui.row().classes('w-full justify-between items-center py-2 border-b border-gray-50 last:border-0'):
                    ui.label(libelle).classes('text-xs text-gray-400')
                    ui.label(valeur).classes(style)

        # --- Modifier le nom ---
        with ui.card().classes('w-full p-4 mb-3'):
            ui.label('Modifier le nom affiché').classes('text-sm font-semibold mb-2')
            nom_input = ui.input('Nouveau nom', value=full_name if full_name != '—' else '').classes('w-full')

            def save_name():
                new_name = (nom_input.value or '').strip()
                if not new_name:
                    notify_error('Le nom ne peut pas être vide.')
                    return
                try:
                    supabase = get_supabase_client()
                    supabase.table('profiles').update({'full_name': new_name}).eq('id', user_id).execute()
                    notify_success('Nom mis à jour avec succès.')
                except Exception as e:
                    notify_error(f'Erreur : {str(e)}')

            ui.button('Enregistrer', on_click=save_name).props('color=positive').classes('w-full mt-2')

        # --- Changer le mot de passe ---
        with ui.card().classes('w-full p-4 mb-3'):
            ui.label('Changer le mot de passe').classes('text-sm font-semibold mb-2')
            new_pw  = ui.input('Nouveau mot de passe', password=True, password_toggle_button=True).classes('w-full')
            conf_pw = ui.input('Confirmer',            password=True, password_toggle_button=True).classes('w-full')

            def change_password():
                p1 = (new_pw.value  or '').strip()
                p2 = (conf_pw.value or '').strip()
                if not p1:
                    notify_error('Saisissez un mot de passe.')
                    return
                if p1 != p2:
                    notify_error('Les mots de passe ne correspondent pas.')
                    return
                if len(p1) < 8:
                    notify_error('Minimum 8 caractères.')
                    return
                try:
                    supabase = get_supabase_client()
                    supabase.auth.update_user({'password': p1})
                    new_pw.value  = ''
                    conf_pw.value = ''
                    notify_success('Mot de passe mis à jour.')
                except Exception as e:
                    notify_error(f'Erreur : {str(e)}')

            ui.button('Mettre à jour', on_click=change_password).props('color=primary').classes('w-full mt-2')

        ui.element('div').style('height: 8px')

        # --- Déconnexion ---
        ui.button(
            'Se déconnecter',
            icon='logout',
            on_click=lambda: ui.navigate.to('/logout')
        ).props('color=negative flat').classes('w-full')

    dashboard_layout(title='Mon Profil', content=content, show_back=True)
