from nicegui import ui

from app.layouts.app_layout import app_layout
from app.components.action_button import render_action_button


def home_page() -> None:
    def content() -> None:
        ui.add_head_html('''
        <style>
            .pm-landing-wrap {
                min-height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                text-align: center;
            }
            .pm-brand-zone {
                margin-top: 34px;
            }
            .pm-brand-mark {
                font-size: 1.8rem;
                font-weight: 800;
                color: #1f5ca8;
                margin-bottom: 10px;
            }
            .pm-brand-sub {
                font-size: 1.15rem;
                font-weight: 700;
                color: #7ebe4e;
                letter-spacing: .05em;
            }
            .pm-landing-meta {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
                margin-top: 40px;
                text-align: left;
                color: #3f4854;
                font-size: .84rem;
            }
            .pm-landing-mode {
                color: #b1b7bf;
                font-size: .8rem;
                margin-top: 2px;
            }
            .pm-landing-actions {
                display: flex;
                flex-direction: column;
                gap: 18px;
                margin: 34px 0 26px 0;
            }
            .pm-landing-footer {
                text-align: center;
                color: #bcc2ca;
                font-size: .88rem;
                margin-top: auto;
                margin-bottom: 16px;
            }
            .pm-power-icon {
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 18px auto 8px auto;
                font-size: 4rem;
                color: #111111;
            }
        </style>
        ''')

        with ui.element('div').classes('pm-landing-wrap'):
            with ui.element('div').classes('pm-brand-zone'):
                ui.label('AFS Impact').classes('pm-brand-mark')
                ui.label('POWER MIND').classes('pm-brand-sub')

            with ui.element('div').classes('pm-landing-meta'):
                with ui.column().classes('gap-0'):
                    ui.label('Date/Heure')
                    ui.label('Mode: AUTO').classes('pm-landing-mode')
                ui.label('Température intérieur')
                ui.label('Température extérieur')

            with ui.element('div').classes('pm-landing-actions'):
                render_action_button('Accéder au chauffage', on_click=lambda: ui.navigate.to('/dashboard'), color='green')
                render_action_button('Accéder aux paramètres', on_click=lambda: ui.navigate.to('/login'), color='coral')

            ui.label('Impact environnemental').classes('pm-landing-footer')
            ui.icon('power_settings_new').classes('pm-power-icon')

    app_layout(content)