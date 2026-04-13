from nicegui import ui

from app.layouts.dashboard_layout import dashboard_layout
from app.components.topbar import render_topbar
from app.components.status_chip import render_status_chip
from app.components.action_button import render_action_button
from app.components.alert_badge import render_alert_badge


def dashboard_page() -> None:
    def content() -> None:
        ui.add_head_html('''
        <style>
            .pm-home-grid {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 8px;
                margin-bottom: 10px;
            }
            .pm-home-meta {
                color: #3f4854;
                font-size: .8rem;
            }
            .pm-home-mode {
                color: #b8bec6;
                font-size: .78rem;
                margin-top: 3px;
            }
            .pm-home-switch {
                margin: 10px 0 14px 0;
            }
            .pm-home-main {
                display: grid;
                grid-template-columns: 1fr 1px 1fr;
                gap: 16px;
                align-items: start;
                min-height: 320px;
            }
            .pm-home-divider {
                width: 1px;
                height: 292px;
                background: #2d2d2d;
                opacity: .65;
                margin: 0 auto;
            }
            .pm-col-center { text-align: center; }
            .pm-mode-title {
                font-size: 2.05rem;
                font-weight: 800;
                margin: 18px 0 24px 0;
                line-height: 1;
            }
            .pm-auto { color: #111111; background: #7fbe53; display: inline-block; padding: 0 4px; }
            .pm-manuel { color: #111111; background: #ef6670; display: inline-block; padding: 0 4px; }
            .pm-chip-stack {
                display: flex;
                flex-direction: column;
                gap: 18px;
                margin-top: 22px;
            }
            .pm-temp-row {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 14px;
                margin-top: 78px;
                margin-bottom: 28px;
            }
            .pm-temp-btn {
                width: 34px;
                height: 34px;
                border-radius: 999px;
                background: #f77a42;
                color: #ffffff;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.7rem;
                box-shadow: 0 10px 18px rgba(0,0,0,.18);
                cursor: pointer;
            }
            .pm-temp-value {
                font-size: 2rem;
                font-weight: 700;
                color: #111111;
            }
            .pm-impact {
                margin-top: 26px;
                color: #b5bcc4;
                font-size: .85rem;
            }
            .pm-arrow-link {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                margin-top: 20px;
                border: 1px solid #8b8b8b;
                padding: 8px 12px;
                color: #111111;
                font-size: .86rem;
                background: white;
                position: relative;
            }
        </style>
        ''')

        with ui.element('div').classes('pm-home-grid'):
            with ui.column().classes('gap-0'):
                ui.label('Date/Heure').classes('pm-home-meta')
                ui.label('Mode: AUTO').classes('pm-home-mode')
            ui.label('Température intérieur').classes('pm-home-meta')
            ui.label('Température extérieur').classes('pm-home-meta')

        with ui.row().classes('pm-home-switch items-center'):
            ui.switch(value=False).props('color=grey size=xs')

        with ui.element('div').classes('pm-home-main'):
            with ui.column().classes('items-start'):
                ui.html('<div class="pm-mode-title pm-auto">AUTO</div>')
                with ui.element('div').classes('pm-chip-stack'):
                    render_status_chip('Mode économique', 'economique')
                    render_status_chip('Mode écologique', 'ecologique')
                    render_status_chip('Mode confort', 'confort')

            ui.element('div').classes('pm-home-divider')

            with ui.column().classes('items-center'):
                ui.html('<div class="pm-mode-title pm-manuel">MANUEL</div>')
                with ui.element('div').classes('pm-temp-row'):
                    ui.html('<div class="pm-temp-btn">+</div>')
                    ui.html('<div class="pm-temp-value">26 °</div>')
                    ui.html('<div class="pm-temp-btn">+</div>')
                ui.button('Choisir conso').props('flat dropdown-icon=expand_more').classes(
                    'bg-[#2d87e8] text-white rounded px-3 py-2 text-xs font-bold normal-case'
                )
                ui.html('<div class="pm-arrow-link">Voir consommation &#10132;</div>')

        ui.label('Impact environnemental').classes('pm-impact')

    dashboard_layout(title='Home', content=content, show_back=True)