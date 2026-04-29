# app/components/sidebar.py
from nicegui import ui
from app.core.session import SessionManager
from app.constants import (
    ROUTE_ADMIN, ROUTE_CONSOMMATION, 
    ROUTE_DATE_HEURE, 
    ROUTE_PROGRAMMATION, 
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
            #{'label': 'Modifier H/D', 'icon': 'calendar_month', 'path': ROUTE_DATE_HEURE},
            {'label': 'Valeurs bases', 'icon': 'tune', 'path': ROUTE_VALEURS_BASES},
            {'label': 'Gérer capteurs', 'icon': 'sensors', 'path': ROUTE_ADMIN_CAPTEURS},
        ]
    else:
        items = [
            {'label': 'Home', 'icon': 'home', 'path': ROUTE_HOME},
            {'label': 'Consommation', 'icon': 'bar_chart', 'path': path_conso},
            #{'label': 'Modifier H/D', 'icon': 'calendar_month', 'path': ROUTE_DATE_HEURE},
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