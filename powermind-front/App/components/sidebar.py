# from nicegui import ui


# DEFAULT_NAV_ITEMS = [
#     {'label': 'Home', 'icon': 'home', 'path': '/home'},
#     {'label': 'Consommation', 'icon': 'bar_chart', 'path': '/consommation', 'active': True},
#     {'label': 'Modifier H/D', 'icon': 'calendar_month', 'path': '/date-heure'},
#     {'label': 'Valeurs bases', 'icon': 'tune', 'path': '/valeurs-bases'},
#     {'label': 'Reset', 'icon': 'restart_alt', 'path': '/reset'},
# ]


# def render_sidebar(drawer, nav_items: list | None = None) -> None:
#     items = nav_items or DEFAULT_NAV_ITEMS

#     ui.add_head_html('''
#     <style>
#         .pm-drawer {
#             width: 300px;
#             height: 100%;
#             background: #ffffff;
#             border-top-right-radius: 28px;
#             border-bottom-right-radius: 28px;
#             box-shadow: 0 18px 42px rgba(0,0,0,.08);
#             padding: 18px 18px 20px 18px;
#             display: flex;
#             flex-direction: column;
#             gap: 14px;
#         }
#         .pm-drawer-close-row {
#             display: flex;
#             align-items: center;
#             justify-content: space-between;
#         }
#         .pm-drawer-close {
#             color: #ea6a73;
#             font-size: 24px;
#             cursor: pointer;
#         }
#         .pm-drawer-profile {
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             gap: 6px;
#             padding: 10px 0 6px 0;
#         }
#         .pm-drawer-name {
#             font-size: 1.45rem;
#             font-weight: 700;
#             color: #39424e;
#             margin-top: 4px;
#         }
#         .pm-drawer-mail {
#             font-size: .92rem;
#             color: #9ba3ad;
#         }
#         .pm-nav-list {
#             display: flex;
#             flex-direction: column;
#             gap: 6px;
#             margin-top: 6px;
#         }
#         .pm-nav-item {
#             display: flex;
#             align-items: center;
#             justify-content: space-between;
#             border-radius: 14px;
#             padding: 12px 14px;
#             cursor: pointer;
#             transition: all .18s ease;
#         }
#         .pm-nav-item:hover {
#             background: #f7f7f8;
#         }
#         .pm-nav-item.active {
#             background: #fff1f2;
#         }
#         .pm-nav-left {
#             display: flex;
#             align-items: center;
#             gap: 12px;
#         }
#         .pm-nav-icon {
#             font-size: 20px;
#             color: #c3c9d1;
#         }
#         .pm-nav-item.active .pm-nav-icon {
#             color: #ea6a73;
#         }
#         .pm-nav-label {
#             font-size: 15px;
#             font-weight: 500;
#             color: #59626d;
#         }
#         .pm-nav-item.active .pm-nav-label {
#             color: #3f4854;
#         }
#         .pm-nav-arrow {
#             font-size: 20px;
#             color: #c3c9d1;
#         }
#         .pm-logout {
#             margin-top: auto;
#             display: flex;
#             align-items: center;
#             gap: 12px;
#             padding: 12px 14px;
#             cursor: pointer;
#         }
#         .pm-logout-label {
#             font-size: 15px;
#             font-weight: 500;
#             color: #3f4854;
#         }
#     </style>
#     ''')

#     with drawer:
#         with ui.element('div').classes('pm-drawer'):
#             with ui.element('div').classes('pm-drawer-close-row'):
#                 ui.icon('close').classes('pm-drawer-close').on('click', drawer.toggle)
#                 ui.label('')

#             with ui.element('div').classes('pm-drawer-profile'):
#                 ui.avatar('https://i.pravatar.cc/120?img=32').classes('w-20 h-20')
#                 ui.label('Johanna Doe').classes('pm-drawer-name')
#                 ui.label('johanna@company.com').classes('pm-drawer-mail')

#             with ui.element('div').classes('pm-nav-list'):
#                 for item in items:
#                     active = item.get('active', False)
#                     item_classes = 'pm-nav-item active' if active else 'pm-nav-item'
#                     with ui.element('div').classes(item_classes).on(
#                         'click', lambda e, path=item['path']: ui.navigate.to(path)
#                     ):
#                         with ui.element('div').classes('pm-nav-left'):
#                             ui.icon(item['icon']).classes('pm-nav-icon')
#                             ui.label(item['label']).classes('pm-nav-label')
#                         ui.icon('chevron_right').classes('pm-nav-arrow')

#             with ui.element('div').classes('pm-logout').on('click', lambda: ui.navigate.to('/logout')):
#                 ui.icon('logout').classes('text-black text-lg')
#                 ui.label('Déconnexion').classes('pm-logout-label')



# # app/components/sidebar.py
# from nicegui import ui
# from app.core.session import SessionManager
# from app.constants import ROUTE_ADMIN, ROUTE_CONSOMMATION, ROUTE_DATE_HEURE, ROUTE_VALEURS_BASES, ROUTE_LOGOUT

# # Menu par défaut pour les utilisateurs
# DEFAULT_NAV_ITEMS = [
#     {'label': 'Home', 'icon': 'home', 'path': '/home'},
#     {'label': 'Consommation', 'icon': 'bar_chart', 'path': ROUTE_CONSOMMATION},
#     {'label': 'Modifier H/D', 'icon': 'calendar_month', 'path': ROUTE_DATE_HEURE},
#     {'label': 'Valeurs bases', 'icon': 'tune', 'path': ROUTE_VALEURS_BASES},
# ]

# # Menu spécifique pour les admins
# ADMIN_NAV_ITEMS = [
#     {'label': 'Admin Home', 'icon': 'admin_panel_settings', 'path': ROUTE_ADMIN},
#     {'label': 'Consommation', 'icon': 'bar_chart', 'path': ROUTE_CONSOMMATION},
#     {'label': 'Modifier H/D', 'icon': 'calendar_month', 'path': ROUTE_DATE_HEURE},
#     {'label': 'Valeurs bases', 'icon': 'tune', 'path': ROUTE_VALEURS_BASES},
# ]

# def render_sidebar(drawer) -> None:
#     # --- LOGIQUE DE SÉLECTION DU MENU ---
#     role = SessionManager.get_role()
#     items = ADMIN_NAV_ITEMS if role in ['admin', 'super_admin'] else DEFAULT_NAV_ITEMS
    
#     # Récupération des infos utilisateur dynamiques
#     user_name = SessionManager.get_full_name() or "Utilisateur"
#     user_mail = SessionManager.get_email() or "email@exemple.com"

#     ui.add_head_html('''
#     <style>
#         .pm-drawer {
#             width: 300px;
#             height: 100%;
#             background: #ffffff;
#             border-top-right-radius: 28px;
#             border-bottom-right-radius: 28px;
#             box-shadow: 0 18px 42px rgba(0,0,0,.08);
#             padding: 18px 18px 20px 18px;
#             display: flex;
#             flex-direction: column;
#             gap: 14px;
#         }
#         .pm-drawer-close-row {
#             display: flex;
#             align-items: center;
#             justify-content: space-between;
#         }
#         .pm-drawer-close {
#             color: #ea6a73;
#             font-size: 24px;
#             cursor: pointer;
#         }
#         .pm-drawer-profile {
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             gap: 6px;
#             padding: 10px 0 6px 0;
#         }
#         .pm-drawer-name {
#             font-size: 1.45rem;
#             font-weight: 700;
#             color: #39424e;
#             margin-top: 4px;
#         }
#         .pm-drawer-mail {
#             font-size: .92rem;
#             color: #9ba3ad;
#         }
#         .pm-nav-list {
#             display: flex;
#             flex-direction: column;
#             gap: 6px;
#             margin-top: 6px;
#         }
#         .pm-nav-item {
#             display: flex;
#             align-items: center;
#             justify-content: space-between;
#             border-radius: 14px;
#             padding: 12px 14px;
#             cursor: pointer;
#             transition: all .18s ease;
#         }
#         .pm-nav-item:hover {
#             background: #f7f7f8;
#         }
#         .pm-nav-item.active {
#             background: #fff1f2;
#         }
#         .pm-nav-left {
#             display: flex;
#             align-items: center;
#             gap: 12px;
#         }
#         .pm-nav-icon {
#             font-size: 20px;
#             color: #c3c9d1;
#         }
#         .pm-nav-item.active .pm-nav-icon {
#             color: #ea6a73;
#         }
#         .pm-nav-label {
#             font-size: 15px;
#             font-weight: 500;
#             color: #59626d;
#         }
#         .pm-nav-item.active .pm-nav-label {
#             color: #3f4854;
#         }
#         .pm-nav-arrow {
#             font-size: 20px;
#             color: #c3c9d1;
#         }
#         .pm-logout {
#             margin-top: auto;
#             display: flex;
#             align-items: center;
#             gap: 12px;
#             padding: 12px 14px;
#             cursor: pointer;
#         }
#         .pm-logout-label {
#             font-size: 15px;
#             font-weight: 500;
#             color: #3f4854;
#         }
#     </style>
#     ''')

#     with drawer:
#         with ui.element('div').classes('pm-drawer'):
#             with ui.element('div').classes('pm-drawer-close-row'):
#                 ui.icon('close').classes('pm-drawer-close').on('click', drawer.toggle)
            
#             with ui.element('div').classes('pm-drawer-profile'):
#                 ui.avatar('https://i.pravatar.cc/120?img=32').classes('w-20 h-20')
#                 # Affichage dynamique du nom et mail
#                 ui.label(user_name).classes('pm-drawer-name')
#                 ui.label(user_mail).classes('pm-drawer-mail')

#             with ui.element('div').classes('pm-nav-list'):
#                 for item in items:
#                     # Gestion de l'état actif (si le chemin actuel correspond au menu)
#                     with ui.element('div').classes('pm-nav-item').on(
#                         'click', lambda e, p=item['path']: ui.navigate.to(p)
#                     ):
#                         with ui.element('div').classes('pm-nav-left'):
#                             ui.icon(item['icon']).classes('pm-nav-icon')
#                             ui.label(item['label']).classes('pm-nav-label')
#                         ui.icon('chevron_right').classes('pm-nav-arrow')

#             # Logout utilise la constante
#             with ui.element('div').classes('pm-logout').on('click', lambda: ui.navigate.to(ROUTE_LOGOUT)):
#                 ui.icon('logout').classes('text-black text-lg')
#                 ui.label('Déconnexion').classes('pm-logout-label')

# app/components/sidebar.py
from nicegui import ui
from app.core.session import SessionManager
from app.constants import (
    ROUTE_ADMIN, ROUTE_CONSOMMATION, ROUTE_DATE_HEURE, ROUTE_PROGRAMMATION, 
    ROUTE_VALEURS_BASES, ROUTE_LOGOUT, ROUTE_HOME, ROUTE_ADMIN_CAPTEURS
)

def render_sidebar(drawer) -> None:
    # --- LOGIQUE DE SESSION ---
    role = SessionManager.get_role()
    inst_id = SessionManager.get_installation_id()
    user_name = SessionManager.get_full_name() or "Utilisateur"
    user_mail = SessionManager.get_email() or "email@exemple.com"

    # --- CONSTRUCTION DES MENUS DYNAMIQUES ---
    # On injecte l'ID d'installation dans le path de Consommation
    path_conso = f"{ROUTE_CONSOMMATION}/{inst_id}" if inst_id else ROUTE_HOME

    if role in ['admin', 'super_admin']:
        items = [
            {'label': 'Admin Home', 'icon': 'admin_panel_settings', 'path': ROUTE_ADMIN},
            {'label': 'Consommation', 'icon': 'bar_chart', 'path': path_conso},
            {'label': 'Modifier H/D', 'icon': 'calendar_month', 'path': ROUTE_DATE_HEURE},
            {'label': 'Valeurs bases', 'icon': 'tune', 'path': ROUTE_VALEURS_BASES},
            {'label': 'Gérer capteurs', 'icon': 'sensors', 'path': ROUTE_ADMIN_CAPTEURS},
        ]
    else:
        items = [
            {'label': 'Home', 'icon': 'home', 'path': ROUTE_HOME},
            {'label': 'Consommation', 'icon': 'bar_chart', 'path': path_conso},
            {'label': 'Modifier H/D', 'icon': 'calendar_month', 'path': ROUTE_DATE_HEURE},
            {'label': 'Valeurs bases', 'icon': 'tune', 'path': ROUTE_VALEURS_BASES},
            {'label': 'Programmation', 'icon': 'event', 'path': ROUTE_PROGRAMMATION}
        ]

    ui.add_head_html('''
    <style>
        .pm-drawer { width: 300px; height: 100%; background: #ffffff; border-top-right-radius: 28px; border-bottom-right-radius: 28px; box-shadow: 0 18px 42px rgba(0,0,0,.08); padding: 18px 18px 20px 18px; display: flex; flex-direction: column; gap: 14px; }
        .pm-drawer-close-row { display: flex; align-items: center; justify-content: space-between; }
        .pm-drawer-close { color: #ea6a73; font-size: 24px; cursor: pointer; }
        .pm-drawer-profile { display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 10px 0 6px 0; }
        .pm-drawer-name { font-size: 1.45rem; font-weight: 700; color: #39424e; margin-top: 4px; }
        .pm-drawer-mail { font-size: .92rem; color: #9ba3ad; }
        .pm-nav-list { display: flex; flex-direction: column; gap: 6px; margin-top: 6px; }
        .pm-nav-item { display: flex; align-items: center; justify-content: space-between; border-radius: 14px; padding: 12px 14px; cursor: pointer; transition: all .18s ease; }
        .pm-nav-item:hover { background: #f7f7f8; }
        .pm-nav-left { display: flex; align-items: center; gap: 12px; }
        .pm-nav-icon { font-size: 20px; color: #c3c9d1; }
        .pm-nav-label { font-size: 15px; font-weight: 500; color: #59626d; }
        .pm-nav-arrow { font-size: 20px; color: #c3c9d1; }
        .pm-logout { margin-top: auto; display: flex; align-items: center; gap: 12px; padding: 12px 14px; cursor: pointer; }
        .pm-logout-label { font-size: 15px; font-weight: 500; color: #3f4854; }
    </style>
    ''')

    with drawer:
        with ui.element('div').classes('pm-drawer'):
            with ui.element('div').classes('pm-drawer-close-row'):
                ui.icon('close').classes('pm-drawer-close').on('click', drawer.toggle)
            
            with ui.element('div').classes('pm-drawer-profile'):
                ui.avatar('https://i.pravatar.cc/120?img=32').classes('w-20 h-20')
                ui.label(user_name).classes('pm-drawer-name')
                # Pastille Admin
                if role in ['admin', 'super_admin']:
                    ui.badge('ADMINISTRATEUR', color='coral').classes('text-[9px] px-2 mb-1')
                ui.label(user_mail).classes('pm-drawer-mail')

            with ui.element('div').classes('pm-nav-list'):
                for item in items:
                    with ui.element('div').classes('pm-nav-item').on(
                        'click', lambda e, p=item['path']: ui.navigate.to(p)
                    ):
                        with ui.element('div').classes('pm-nav-left'):
                            ui.icon(item['icon']).classes('pm-nav-icon')
                            ui.label(item['label']).classes('pm-nav-label')
                        ui.icon('chevron_right').classes('pm-nav-arrow')

            with ui.element('div').classes('pm-logout').on('click', lambda: ui.navigate.to(ROUTE_LOGOUT)):
                ui.icon('logout').classes('text-black text-lg')
                ui.label('Déconnexion').classes('pm-logout-label')