# import traceback
# from nicegui import ui

# from app.core.notifications import notify_error, notify_success
# from app.core.security import get_default_redirect_path
# from app.core.session import SessionManager
# from app.core.supabase_client import SupabaseConfigError, is_supabase_configured
# from app.core.utils import parse_uuid
# from app.layouts.auth_layout import auth_layout
# from app.components.forms import render_input_field
# from app.components.action_button import render_action_button
# from app.services.auth_service import AuthService


# def login_page() -> None:
#     def content() -> None:
#         ui.add_head_html('''
#         <style>
#             .pm-auth-title {
#                 font-size: 2rem;
#                 font-weight: 700;
#                 color: #3f4854;
#                 margin-top: 42px;
#                 margin-bottom: 30px;
#             }
#             .pm-auth-note {
#                 text-align: center;
#                 margin-top: 20px;
#                 color: #b1b7bf;
#                 font-size: .8rem;
#             }
#             .pm-auth-links {
#                 display: flex;
#                 justify-content: space-between;
#                 margin-top: 8px;
#                 font-size: .82rem;
#                 gap: 12px;
#                 flex-wrap: wrap;
#             }
#             .pm-auth-links a {
#                 color: #ea6a73;
#                 text-decoration: none;
#             }
#             .pm-auth-warning {
#                 margin-top: 12px;
#                 padding: 10px 12px;
#                 border-radius: 10px;
#                 background: #fff4f4;
#                 color: #b54747;
#                 font-size: .85rem;
#                 text-align: center;
#             }
#         </style>
#         ''')

#         is_loading = {'value': False}
#         supabase_ready = is_supabase_configured()

#         def handle_login() -> None:
#             if is_loading['value']:
#                 return

#             user_identifier = (identifiant.value or '').strip()
#             user_password = mot_de_passe.value or ''

#             if not user_identifier or not user_password:
#                 notify_error('Merci de renseigner l’identifiant et le mot de passe.')
#                 return

#             is_loading['value'] = True

#             try:
#                 auth_service = AuthService()
#                 result = auth_service.login_user(
#                     identifier=user_identifier,
#                     password=user_password,
#                 )

#                 if not result or not result.get('success'):
#                     # Log l'échec métier dans le terminal
#                     print(f"--- ÉCHEC CONNEXION : {result.get('message') if result else 'Résultat vide'} ---")
#                     notify_error(
#                         result.get('message', 'Connexion impossible.')
#                         if result else 'Connexion impossible.'
#                     )
#                     return

#                 user = result.get('user') or {}
#                 profile = result.get('profile') or {}
#                 installation = result.get('installation') or {}

#                 installation_id = installation.get('id')
#                 installation_uuid = parse_uuid(installation_id) if installation_id else None

#                 SessionManager.set_user_session(
#                     user_id=str(user.get('id') or ''),
#                     email=str(user.get('email') or user_identifier),
#                     role=str(profile.get('role') or 'user'),
#                     installation_id=str(installation_uuid) if installation_uuid else None,
#                     profile_id=str(profile.get('id') or ''),
#                     full_name=str(profile.get('full_name') or ''),
#                 )

#                 notify_success('Connexion réussie.')

#                 redirect_path = (
#                     f'/dashboard/{installation_uuid}'
#                     if installation_uuid
#                     else get_default_redirect_path()
#                 )
#                 ui.navigate.to(redirect_path)

#             except SupabaseConfigError as e:
#                 print(f"--- ERREUR CONFIGURATION SUPABASE ---\n{e}")
#                 notify_error("Configuration d’authentification incomplète côté serveur.")
#             except Exception as e:
#                 # DEBUG COMPLET DANS LE TERMINAL
#                 print("\n" + "="*50)
#                 print("ERREUR CRITIQUE LORS DE LA CONNEXION :")
#                 print(f"Type : {type(e).__name__}")
#                 print(f"Détails : {str(e)}")
#                 print("-" * 50)
#                 traceback.print_exc()
#                 print("="*50 + "\n")
                
#                 notify_error('Une erreur est survenue lors de la connexion. Veuillez réessayer.')
#             finally:
#                 is_loading['value'] = False

#         ui.icon('arrow_back').classes(
#             'text-[#ea6a73] text-2xl cursor-pointer mt-2'
#         ).on('click', lambda: ui.navigate.to('/'))

#         ui.label('Connexion').classes('pm-auth-title')

#         identifiant = render_input_field('Identifiant', 'Votre identifiant ou email')
#         mot_de_passe = render_input_field('Mot de passe', 'Votre mot de passe', password=True)
#         mot_de_passe.on('keydown.enter', lambda _: handle_login())

#         with ui.element('div').classes('pm-auth-links'):
#             ui.link('Créer un compte', '/register')
#             ui.link('Mot de passe oublié', '/forgot-password')

#         if not supabase_ready:
#             ui.label(
#                 "La configuration Supabase est absente. La connexion est temporairement indisponible."
#             ).classes('pm-auth-warning')

#         ui.element('div').style('height: 30px')
#         render_action_button('S’identifier', on_click=handle_login, color='coral')

#         ui.label('Accédez à votre espace PowerMind.').classes('pm-auth-note')

#     auth_layout(content)

import traceback
from nicegui import ui

from app.core.notifications import notify_error, notify_success
from app.core.security import get_default_redirect_path
from app.core.session import SessionManager
from app.core.supabase_client import SupabaseConfigError, is_supabase_configured
from app.core.utils import parse_uuid
from app.layouts.auth_layout import auth_layout
from app.components.forms import render_input_field
from app.components.action_button import render_action_button
from app.services.auth_service import AuthService
# Import des constantes de routes
from app.constants import ROUTE_ADMIN, ROUTE_DASHBOARD, ROUTE_WAITING, ROUTE_LOGIN, ROUTE_REGISTER, ROUTE_FORGOT_PASSWORD


def login_page() -> None:
    def content() -> None:
        ui.add_head_html('''
        <style>
            .pm-auth-title { font-size: 2rem; font-weight: 700; color: #3f4854; margin-top: 42px; margin-bottom: 30px; }
            .pm-auth-note { text-align: center; margin-top: 20px; color: #b1b7bf; font-size: .8rem; }
            .pm-auth-links { display: flex; justify-content: space-between; margin-top: 8px; font-size: .82rem; gap: 12px; flex-wrap: wrap; }
            .pm-auth-links a { color: #ea6a73; text-decoration: none; }
            .pm-auth-warning { margin-top: 12px; padding: 10px 12px; border-radius: 10px; background: #fff4f4; color: #b54747; font-size: .85rem; text-align: center; }
        </style>
        ''')

        is_loading = {'value': False}
        supabase_ready = is_supabase_configured()

        def handle_login() -> None:
            if is_loading['value']:
                return

            user_identifier = (identifiant.value or '').strip()
            user_password = mot_de_passe.value or ''

            if not user_identifier or not user_password:
                notify_error('Merci de renseigner l’identifiant et le mot de passe.')
                return

            is_loading['value'] = True

            try:
                auth_service = AuthService()
                result = auth_service.login_user(
                    identifier=user_identifier,
                    password=user_password,
                )

                if not result or not result.get('success'):
                    print(f"--- ÉCHEC CONNEXION : {result.get('message') if result else 'Résultat vide'} ---")
                    notify_error(result.get('message', 'Connexion impossible.'))
                    return

                user = result.get('user') or {}
                profile = result.get('profile') or {}
                installation = result.get('installation') or {}

                installation_id = installation.get('id')
                installation_uuid = parse_uuid(installation_id) if installation_id else None
                
                # Récupération du rôle pour la logique de redirection
                user_role = str(profile.get('role') or 'user')

                SessionManager.set_user_session(
                    user_id=str(user.get('id') or ''),
                    email=str(user.get('email') or user_identifier),
                    role=user_role,
                    installation_id=str(installation_uuid) if installation_uuid else None,
                    profile_id=str(profile.get('id') or ''),
                    full_name=str(profile.get('full_name') or ''),
                )

                notify_success('Connexion réussie.')

                # --- LOGIQUE DE REDIRECTION INTELLIGENTE ---
                if user_role in ['admin', 'super_admin']:
                    # 1. Admin -> Direction Gestion Utilisateurs
                    ui.navigate.to(ROUTE_ADMIN)
                
                elif installation_uuid:
                    # 2. User avec installation -> Direction Dashboard
                    ui.navigate.to(f'{ROUTE_DASHBOARD}/{installation_uuid}')
                
                else:
                    # 3. User sans installation -> Direction Page d'attente (Service Commercial)
                    ui.navigate.to(ROUTE_WAITING)

            except SupabaseConfigError as e:
                print(f"--- ERREUR CONFIGURATION SUPABASE ---\n{e}")
                notify_error("Configuration d’authentification incomplète côté serveur.")
            except Exception as e:
                print("\n" + "="*50)
                print("ERREUR CRITIQUE LORS DE LA CONNEXION :")
                print(f"Type : {type(e).__name__}")
                print(f"Détails : {str(e)}")
                print("-" * 50)
                traceback.print_exc()
                print("="*50 + "\n")
                notify_error('Une erreur est survenue lors de la connexion.')
            finally:
                is_loading['value'] = False

        ui.icon('arrow_back').classes('text-[#ea6a73] text-2xl cursor-pointer mt-2').on('click', lambda: ui.navigate.to('/'))
        ui.label('Connexion').classes('pm-auth-title')

        identifiant = render_input_field('Identifiant', 'Votre identifiant ou email')
        mot_de_passe = render_input_field('Mot de passe', 'Votre mot de passe', password=True)
        mot_de_passe.on('keydown.enter', lambda _: handle_login())

        with ui.element('div').classes('pm-auth-links'):
            ui.link('Créer un compte', ROUTE_REGISTER)
            ui.link('Mot de passe oublié', ROUTE_FORGOT_PASSWORD)

        if not supabase_ready:
            ui.label("La configuration Supabase est absente.").classes('pm-auth-warning')

        ui.element('div').style('height: 30px')
        render_action_button('S’identifier', on_click=handle_login, color='coral')
        ui.label('Accédez à votre espace PowerMind.').classes('pm-auth-note')

    auth_layout(content)