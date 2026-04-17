# app/pages/home_page.py

from datetime import datetime
from uuid import UUID
from nicegui import ui

from app.layouts.app_layout import app_layout
from app.components.action_button import render_action_button
from app.core.session import SessionManager
from app.services.mesure_service import MesureService
from app.services.choix_auto_service import ChoixAutoService
from app.constants import ROUTE_LOGIN, ROUTE_DASHBOARD, ROUTE_VALEURS_BASES

# Affichage lisible — gère aussi les anciennes valeurs 'electric'/'gaz'
MODE_DISPLAY: dict[str, str] = {
    'confort':    'CONFORT',
    'ecologique': 'ÉCOLOGIQUE',
    'economique': 'ÉCONOMIQUE',
    'electric':   'ÉLECTRIQUE',
    'gaz':        'GAZ',
}


def home_page() -> None:
    mesure_service = MesureService()
    choix_service  = ChoixAutoService()

    inst_id_str = SessionManager.get_installation_id()
    inst_id = UUID(inst_id_str) if inst_id_str else None

    def content() -> None:
        def handle_navigation(target):
            if not SessionManager.is_authenticated():
                ui.navigate.to(ROUTE_LOGIN)
                return
            ui.navigate.to(ROUTE_DASHBOARD if target == 'chauffage' else ROUTE_VALEURS_BASES)

        # Récupère le choix propre à CETTE installation (pas global)
        mode_text = 'MANUEL'
        if inst_id:
            current_choix = choix_service.get_by_installation(inst_id)
            if current_choix:
                raw = current_choix.choix
                mode_text = MODE_DISPLAY.get(raw, raw.upper())

        temp_int = 'N/A'
        temp_ext = 'N/A'
        if inst_id:
            recent = mesure_service.list_by_installation(inst_id, limit=10)
            for m in recent:
                tm   = m.get('types_mesure') or {}
                code = tm.get('code')
                if code == 'TEMP_INT' and temp_int == 'N/A':
                    temp_int = f"{m.get('value', '?')}°C"
                if code == 'TEMP_EXT' and temp_ext == 'N/A':
                    temp_ext = f"{m.get('value', '?')}°C"

        ui.add_head_html('''
        <style>
            .pm-landing-wrap {
                min-height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                text-align: center;
            }
            .pm-brand-zone { margin-top: 34px; }
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
                    ui.label(datetime.now().strftime('%d/%m/%Y'))
                    ui.label(datetime.now().strftime('%H:%M')).style('font-weight: 700')
                    ui.label(f'Mode: {mode_text}').classes('pm-landing-mode')

                with ui.column().classes('gap-0'):
                    ui.label('Temp. intérieur')
                    ui.label(temp_int).style('font-weight: 700; font-size: 1rem')

                with ui.column().classes('gap-0'):
                    ui.label('Temp. extérieur')
                    ui.label(temp_ext).style('font-weight: 700; font-size: 1rem')

            with ui.element('div').classes('pm-landing-actions'):
                render_action_button('Accéder au chauffage',
                                     on_click=lambda: handle_navigation('chauffage'),
                                     color='green')
                render_action_button('Accéder aux paramètres',
                                     on_click=lambda: handle_navigation('parametres'),
                                     color='coral')

            ui.label('Impact environnemental').classes('pm-landing-footer')
            ui.icon('power_settings_new').classes('pm-power-icon')

    app_layout(content)
