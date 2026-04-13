from nicegui import ui
from components.layout import create_dashboard_layout
# from pages.base import base_content
from pages.home import home_content
# from pages.modif import modif_content
# from pages.profil import profil_content

# ----- PAGES PRINCIPALES -----
@ui.page('/dashboard')
def dashboard_page():
    ui.page_title('SUIVI4K - Dashboard')
    create_dashboard_layout(' Dashboard Home', home_content)

# @ui.page('/dashboard/home')
# def dashboard_home():
#     create_dashboard_layout(' Home', home_content)

# @ui.page('/dashboard/profil')
# def dashboard_profil():
#     create_dashboard_layout(' Modifier Profil', profil_content)

# @ui.page('/dashboard/modif')
# def dashboard_modif():
#     create_dashboard_layout(' Modifier Heure/Date', modif_content)

# @ui.page('/dashboard/base')
# def dashboard_base():
#     create_dashboard_layout('Valeurs', base_content)
