# app/routes.py

from nicegui import app, ui

from app.constants import (
    DEFAULT_REDIRECT_IF_NOT_AUTHENTICATED,
    ROUTE_404,
    ROUTE_ALERTES,
    ROUTE_CAPTEURS,
    ROUTE_CONSOMMATION,
    ROUTE_DASHBOARD,
    #ROUTE_DATE_HEURE,
    ROUTE_HOME,
    ROUTE_INSTALLATIONS,
    ROUTE_LOGIN,
    ROUTE_LOGOUT,
    ROUTE_ADMIN,
    ROUTE_MAINTENANCE,
    ROUTE_MESURES,
    ROUTE_FORBIDEN,
    ROUTE_PROFIL,
    ROUTE_REGLAGES,
    ROUTE_REGISTER,
    ROUTE_ROOT,
    ROUTE_VALEURS_BASES,
    ROUTE_WAITING,
    ROUTE_PROGRAMMATION,
    ROUTE_ADMIN_CAPTEURS,
)
from app.core.security import require_auth, require_role
from app.core.session import SessionManager
from app.pages.alertes_page import alertes_page
from app.pages.capteurs_page import capteurs_page
from app.pages.consommation_page import consommation_page
from app.pages.dashboard_page import dashboard_page
from app.pages.date_heure_page import date_heure_page
from app.pages.home_page import home_page
from app.pages.admin.users_page import admin_users_page
from app.pages.installations_page import installations_page
from app.pages.login_page import login_page
from app.pages.maintenance_page import maintenance_page
from app.pages.mesures_page import mesures_page
from app.pages.profil_page import profil_page
from app.pages.register_page import register_page
from app.pages.reglages_page import reglages_page
from app.pages.valeurs_bases_page import valeurs_bases_page
from app.pages.forgot_password_page import forgot_password_page
from app.pages.waiting_page import waiting_activation_page
from app.pages.programmation_page import programmation_page
from app.pages.admin.admin_capteurs_page import admin_capteurs_page


def is_authenticated() -> bool:
    return bool(app.storage.user.get('authenticated', False))


# def get_dashboard_route() -> str:
#     installation_id = SessionManager.get_installation_id()
#     if installation_id:
#         return f'{ROUTE_DASHBOARD}/{installation_id}'
#     return ROUTE_LOGIN
def get_dashboard_route() -> str:
    # On récupère le rôle et l'ID d'installation
    role = SessionManager.get_role()
    installation_id = SessionManager.get_installation_id()
    
    if role in ['admin', 'super_admin']:
        return ROUTE_ADMIN
    
    if installation_id:
        return f'{ROUTE_DASHBOARD}/{installation_id}'
    
    # Si c'est un utilisateur sans installation, on l'envoie vers la page d'attente
    return ROUTE_WAITING

# def redirect_to_default_page() -> None:
#     if is_authenticated():
#         ui.navigate.to(get_dashboard_route())
#     else:
#         ui.navigate.to(ROUTE_LOGIN)
def redirect_to_default_page() -> None:
    if is_authenticated():
        target = get_dashboard_route()
        # Sécurité : si on est déjà sur la cible, on ne navigue pas pour éviter la boucle
        ui.navigate.to(target)
    else:
        ui.navigate.to(ROUTE_LOGIN)

def register_routes() -> None:

    # --- Racine ---
    @ui.page(ROUTE_ROOT)
    def root_page():
        redirect_to_default_page()

    # --- Auth (publiques) ---
    @ui.page(ROUTE_LOGIN)
    def login():
        if is_authenticated():
            ui.navigate.to(get_dashboard_route())
        else:
            login_page()

    @ui.page(ROUTE_REGISTER)
    def register():
        register_page()

    @ui.page(ROUTE_LOGOUT)
    def logout():
        SessionManager.clear()
        ui.navigate.to(ROUTE_LOGIN)

    # --- Admin (rôle requis) ---
    @ui.page(ROUTE_ADMIN)
    def admin_users():
        if not require_role('admin', 'super_admin'):
            return
        admin_users_page()

    # --- Dashboard ---
    @ui.page(ROUTE_DASHBOARD + '/{installation_id}')
    def dashboard(installation_id: str):
        if not require_auth():
            return
        dashboard_page(installation_id)

    @ui.page(ROUTE_DASHBOARD)
    def dashboard_redirect():
        if not require_auth():
            return
        redirect_to_default_page()

    # --- Pages principales (toutes sécurisées) ---
    @ui.page(ROUTE_HOME)
    def home():
        if not require_auth():
            return
        home_page()

    @ui.page(ROUTE_INSTALLATIONS)
    def installations():
        if not require_auth():
            return
        installations_page()

    @ui.page(ROUTE_CAPTEURS + '/{installation_id}')
    def capteurs(installation_id: str):
        if not require_auth():
            return
        capteurs_page(installation_id)

    @ui.page(ROUTE_MESURES + '/{installation_id}')
    def mesures(installation_id: str):
        if not require_auth():
            return
        mesures_page(installation_id)

    @ui.page(ROUTE_ALERTES + '/{installation_id}')
    def alertes(installation_id: str):
        if not require_auth():
            return
        alertes_page(installation_id)

    @ui.page(ROUTE_CONSOMMATION + '/{installation_id}')
    def consommation_route(installation_id: str):
        if not require_auth():
            return
        consommation_page(installation_id)

    @ui.page(ROUTE_VALEURS_BASES)
    def valeurs_bases():
        if not require_auth():
            return
        valeurs_bases_page()

    # @ui.page(ROUTE_DATE_HEURE)
    # def date_heure():
    #     if not require_auth():
    #         return
    #     date_heure_page()

    @ui.page(ROUTE_PROFIL)
    def profil():
        if not require_auth():
            return
        profil_page()

    @ui.page(ROUTE_REGLAGES)
    def reglages():
        if not require_role('admin', 'technicien'):
            return
        reglages_page()

    @ui.page(ROUTE_MAINTENANCE)
    def maintenance():
        if not require_role('admin', 'technicien'):
            return
        maintenance_page()

    @ui.page('/forgot-password')
    def forgot_password():
        forgot_password_page()

    @ui.page('/reset-password')
    def reset_password():
        # Page intermédiaire : Supabase redirige ici après clic sur le lien email.
        # Le token est dans l'URL (#access_token=...), géré côté JS par Supabase.
        from nicegui import ui
        from app.layouts.auth_layout import auth_layout

        def content():
            ui.label('Nouveau mot de passe').classes('pm-auth-title')
            ui.label('Saisissez votre nouveau mot de passe.').classes('text-sm text-gray-400 mb-4')

            new_pw  = ui.input('Nouveau mot de passe', password=True, password_toggle_button=True).classes('w-full')
            conf_pw = ui.input('Confirmer',            password=True, password_toggle_button=True).classes('w-full')

            def do_reset():
                p1 = (new_pw.value  or '').strip()
                p2 = (conf_pw.value or '').strip()
                if not p1 or p1 != p2:
                    ui.notify('Les mots de passe ne correspondent pas.', type='negative')
                    return
                if len(p1) < 8:
                    ui.notify('Minimum 8 caractères.', type='negative')
                    return
                try:
                    from app.core.supabase_client import get_supabase_client
                    supabase = get_supabase_client()
                    supabase.auth.update_user({'password': p1})
                    ui.notify('Mot de passe mis à jour ! Redirection…', type='positive')
                    ui.timer(1.5, lambda: ui.navigate.to('/login'), once=True)
                except Exception as e:
                    ui.notify(f'Erreur : {str(e)}', type='negative')

            ui.element('div').style('height: 12px')
            ui.button('Confirmer le nouveau mot de passe', on_click=do_reset).props('color=positive').classes('w-full')

        auth_layout(content)

    # --- Erreurs ---
    @ui.page(ROUTE_FORBIDEN)
    def forbiden():
        ui.label('403 — Accès interdit').classes('text-xl font-bold text-red-500 p-8')
        ui.button('Retour', on_click=lambda: ui.navigate.to(get_dashboard_route()))

    @ui.page(ROUTE_404)
    def not_found():
        ui.label('404 — Page non trouvée').classes('text-xl font-bold p-8')
        ui.button('Retour', on_click=lambda: ui.navigate.to('/'))

    @ui.page(ROUTE_WAITING)
    def waiting_room():
        waiting_activation_page()
        
    @ui.page(ROUTE_PROGRAMMATION)
    def programmation():
        if not require_auth():
            return
        programmation_page()
        
    @ui.page(ROUTE_ADMIN_CAPTEURS)
    def admin_capteurs():
        if not require_role('admin', 'super_admin'):
            return
        from app.pages.admin.admin_capteurs_page import admin_capteurs_page
        admin_capteurs_page()