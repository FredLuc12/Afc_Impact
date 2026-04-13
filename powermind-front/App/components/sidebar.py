from nicegui import ui


DEFAULT_NAV_ITEMS = [
    {'label': 'Home', 'icon': 'home', 'path': '/home'},
    {'label': 'Consommation', 'icon': 'bar_chart', 'path': '/consommation', 'active': True},
    {'label': 'Modifier H/D', 'icon': 'calendar_month', 'path': '/date-heure'},
    {'label': 'Valeurs bases', 'icon': 'tune', 'path': '/valeurs-bases'},
    {'label': 'Reset', 'icon': 'restart_alt', 'path': '/reset'},
]


def render_sidebar(drawer, nav_items: list | None = None) -> None:
    items = nav_items or DEFAULT_NAV_ITEMS

    ui.add_head_html('''
    <style>
        .pm-drawer {
            width: 300px;
            height: 100%;
            background: #ffffff;
            border-top-right-radius: 28px;
            border-bottom-right-radius: 28px;
            box-shadow: 0 18px 42px rgba(0,0,0,.08);
            padding: 18px 18px 20px 18px;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }
        .pm-drawer-close-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .pm-drawer-close {
            color: #ea6a73;
            font-size: 24px;
            cursor: pointer;
        }
        .pm-drawer-profile {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            padding: 10px 0 6px 0;
        }
        .pm-drawer-name {
            font-size: 1.45rem;
            font-weight: 700;
            color: #39424e;
            margin-top: 4px;
        }
        .pm-drawer-mail {
            font-size: .92rem;
            color: #9ba3ad;
        }
        .pm-nav-list {
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-top: 6px;
        }
        .pm-nav-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-radius: 14px;
            padding: 12px 14px;
            cursor: pointer;
            transition: all .18s ease;
        }
        .pm-nav-item:hover {
            background: #f7f7f8;
        }
        .pm-nav-item.active {
            background: #fff1f2;
        }
        .pm-nav-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .pm-nav-icon {
            font-size: 20px;
            color: #c3c9d1;
        }
        .pm-nav-item.active .pm-nav-icon {
            color: #ea6a73;
        }
        .pm-nav-label {
            font-size: 15px;
            font-weight: 500;
            color: #59626d;
        }
        .pm-nav-item.active .pm-nav-label {
            color: #3f4854;
        }
        .pm-nav-arrow {
            font-size: 20px;
            color: #c3c9d1;
        }
        .pm-logout {
            margin-top: auto;
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 14px;
            cursor: pointer;
        }
        .pm-logout-label {
            font-size: 15px;
            font-weight: 500;
            color: #3f4854;
        }
    </style>
    ''')

    with drawer:
        with ui.element('div').classes('pm-drawer'):
            with ui.element('div').classes('pm-drawer-close-row'):
                ui.icon('close').classes('pm-drawer-close').on('click', drawer.toggle)
                ui.label('')

            with ui.element('div').classes('pm-drawer-profile'):
                ui.avatar('https://i.pravatar.cc/120?img=32').classes('w-20 h-20')
                ui.label('Johanna Doe').classes('pm-drawer-name')
                ui.label('johanna@company.com').classes('pm-drawer-mail')

            with ui.element('div').classes('pm-nav-list'):
                for item in items:
                    active = item.get('active', False)
                    item_classes = 'pm-nav-item active' if active else 'pm-nav-item'
                    with ui.element('div').classes(item_classes).on(
                        'click', lambda e, path=item['path']: ui.navigate.to(path)
                    ):
                        with ui.element('div').classes('pm-nav-left'):
                            ui.icon(item['icon']).classes('pm-nav-icon')
                            ui.label(item['label']).classes('pm-nav-label')
                        ui.icon('chevron_right').classes('pm-nav-arrow')

            with ui.element('div').classes('pm-logout').on('click', lambda: ui.navigate.to('/logout')):
                ui.icon('logout').classes('text-black text-lg')
                ui.label('Déconnexion').classes('pm-logout-label')