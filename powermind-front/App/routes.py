# app/routes.py

from nicegui import app, ui

from app.constants import (
    DEFAULT_REDIRECT_IF_NOT_AUTHENTICATED,
    ROUTE_404,
    ROUTE_ALERTES,
    ROUTE_CAPTEURS,
    ROUTE_CONSOMMATION,
    ROUTE_DASHBOARD,
    ROUTE_DATE_HEURE,
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
)
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
from app.core.session import SessionManager

def is_authenticated() -> bool:
    return bool(app.storage.user.get('authenticated', False))

def get_dashboard_route() -> str:
    installation_id = SessionManager.get_installation_id()
    if installation_id:
        return f'{ROUTE_DASHBOARD}/{installation_id}'
    return ROUTE_LOGIN

def redirect_to_default_page() -> None:
    if is_authenticated():
        ui.navigate.to(get_dashboard_route())
    else:
        ui.navigate.to(ROUTE_LOGIN)

def register_routes() -> None:
    # 1. Racine
    @ui.page(ROUTE_ROOT)
    def root_page():
        redirect_to_default_page()

    # 2. Auth
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

    # 3. Admin
    @ui.page(ROUTE_ADMIN)
    def admin_users():
        if app.storage.user.get('role') not in ['admin', 'super_admin']:
            ui.navigate.to(get_dashboard_route())
            return
        admin_users_page()

    # 4. App Pages
    @ui.page(ROUTE_DASHBOARD + '/{installation_id}')
    def dashboard(installation_id: str):
        dashboard_page(installation_id)
    
    # À ajouter dans register_routes() de app/routes.py
    @ui.page(ROUTE_DASHBOARD)
    def dashboard_redirect():
        # On redirige vers l'ID stocké en session
        redirect_to_default_page()

    @ui.page(ROUTE_CAPTEURS + '/{installation_id}')
    def capteurs(installation_id: str):
        capteurs_page(installation_id)

    @ui.page(ROUTE_ALERTES + '/{installation_id}')
    def alertes(installation_id: str):
        alertes_page(installation_id)

    @ui.page(ROUTE_CONSOMMATION + '/{installation_id}')
    def consommation_route(installation_id: str):
        consommation_page(installation_id)
        
    @ui.page(ROUTE_DATE_HEURE)
    def date_heure():
        date_heure_page()
    
    @ui.page(ROUTE_VALEURS_BASES)
    def valeurs_bases():
        valeurs_bases_page()
    
    @ui.page(ROUTE_MESURES + '/{installation_id}')
    def mesures(installation_id: str):
        mesures_page(installation_id)
        
    @ui.page(ROUTE_PROFIL)
    def profil():
        profil_page()
        
    @ui.page(ROUTE_REGLAGES)
    def reglages():
        reglages_page()
    
    @ui.page(ROUTE_MAINTENANCE)
    def maintenance():
        maintenance_page()
    
    # 6. Forbiden
    @ui.page(ROUTE_FORBIDEN)
    def forbiden():
        ui.label('403 - Accès interdit')
        ui.button('Retour', on_click=lambda: ui.navigate.to(get_dashboard_route()))

    # 5. Autres (Simple)
    @ui.page(ROUTE_HOME)
    def home(): home_page()
    
    @ui.page(ROUTE_INSTALLATIONS)
    def installations(): installations_page()
    
    @ui.page(ROUTE_PROFIL)
    def profil(): profil_page()

    @ui.page(ROUTE_404)
    def not_found():
        ui.label('404 - Page non trouvée')
        ui.button('Retour', on_click=lambda: ui.navigate.to('/'))
