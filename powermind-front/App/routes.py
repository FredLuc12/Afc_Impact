# app/routes.py

from nicegui import ui

from app.constants import (
    DEFAULT_REDIRECT_IF_AUTHENTICATED,
    DEFAULT_REDIRECT_IF_NOT_AUTHENTICATED,
    ROUTE_404,
    ROUTE_ALERTES,
    ROUTE_CAPTEURS,
    ROUTE_DASHBOARD,
    ROUTE_HOME,
    ROUTE_INSTALLATIONS,
    ROUTE_LOGIN,
    ROUTE_LOGOUT,
    ROUTE_MAINTENANCE,
    ROUTE_MESURES,
    ROUTE_PROFIL,
    ROUTE_REGLAGES,
    ROUTE_ROOT,
)
from app.pages.alertes_page import alertes_page
from app.pages.capteurs_page import capteurs_page
from app.pages.dashboard_page import dashboard_page
from app.pages.home_page import home_page
from app.pages.installations_page import installations_page
from app.pages.login_page import login_page
from app.pages.maintenance_page import maintenance_page
from app.pages.mesures_page import mesures_page
from app.pages.profil_page import profil_page
from app.pages.reglages_page import reglages_page


def is_authenticated() -> bool:
    """
    À brancher plus tard sur Supabase/Auth réelle.
    Pour l'instant, retourne False par défaut.
    """
    return False


def redirect_to_default_page() -> None:
    if is_authenticated():
        ui.navigate.to(DEFAULT_REDIRECT_IF_AUTHENTICATED)
    ui.navigate.to(DEFAULT_REDIRECT_IF_NOT_AUTHENTICATED)


def register_routes() -> None:
    @ui.page(ROUTE_ROOT)
    def root_page():
        redirect_to_default_page()

    @ui.page(ROUTE_LOGIN)
    def login():
        login_page()

    @ui.page(ROUTE_LOGOUT)
    def logout():
        ui.notify('Déconnexion en cours...', type='info')
        ui.navigate.to(ROUTE_LOGIN)

    @ui.page(ROUTE_HOME)
    def home():
        home_page()

    @ui.page(ROUTE_DASHBOARD)
    def dashboard():
        dashboard_page()

    @ui.page(ROUTE_INSTALLATIONS)
    def installations():
        installations_page()

    @ui.page(ROUTE_CAPTEURS)
    def capteurs():
        capteurs_page()

    @ui.page(ROUTE_MESURES)
    def mesures():
        mesures_page()

    @ui.page(ROUTE_ALERTES)
    def alertes():
        alertes_page()

    @ui.page(ROUTE_PROFIL)
    def profil():
        profil_page()

    @ui.page(ROUTE_REGLAGES)
    def reglages():
        reglages_page()

    @ui.page(ROUTE_MAINTENANCE)
    def maintenance():
        maintenance_page()

    @ui.page(ROUTE_404)
    def not_found():
        with ui.column().classes('w-full h-screen items-center justify-center gap-4'):
            ui.icon('error_outline').classes('text-6xl text-red-500')
            ui.label('404 - Page non trouvée').classes('text-2xl font-bold')
            ui.label('La page demandée n’existe pas ou n’est plus disponible.').classes('text-gray-500')
            ui.button('Retour au dashboard', on_click=lambda: ui.navigate.to(ROUTE_DASHBOARD))