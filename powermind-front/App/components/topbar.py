from nicegui import ui


def render_topbar(title: str, drawer=None, show_back: bool = False) -> None:
    ui.add_head_html('''
    <style>
        .pm-topbar-wrap { width: 100%; margin-bottom: 18px; }
        .pm-topbar-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding-top: 4px;
        }
        .pm-topbar-left {
            display: flex;
            align-items: center;
            gap: 12px;
            min-width: 0;
        }
        .pm-topbar-icon {
            color: #ea6a73;
            font-size: 24px;
            cursor: pointer;
            line-height: 1;
        }
        .pm-topbar-title {
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
            line-height: 1.1;
            color: #3f4854;
            letter-spacing: -0.02em;
        }
        .pm-topbar-line {
            position: relative;
            width: 100%;
            height: 2px;
            background: #ececec;
            border-radius: 999px;
            margin-top: 16px;
        }
        .pm-topbar-line::after {
            content: '';
            position: absolute;
            right: 0;
            top: 0;
            width: 42%;
            height: 2px;
            border-radius: 999px;
            background: #454d58;
        }
    </style>
    ''')

    with ui.element('div').classes('pm-topbar-wrap'):
        with ui.element('div').classes('pm-topbar-row'):
            with ui.element('div').classes('pm-topbar-left'):
                if show_back:
                    ui.icon('arrow_back').classes('pm-topbar-icon').on('click', lambda: ui.navigate.back())
                elif drawer is not None:
                    ui.icon('menu').classes('pm-topbar-icon').on('click', drawer.toggle)
                else:
                    ui.icon('radio_button_unchecked').classes('pm-topbar-icon opacity-0')

                ui.label(title).classes('pm-topbar-title')
            ui.label('')

        ui.element('div').classes('pm-topbar-line')