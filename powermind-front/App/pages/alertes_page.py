from nicegui import ui

from app.layouts.dashboard_layout import dashboard_layout
from app.components.alert_badge import render_alert_badge
from app.components.stat_card import render_stat_card


def alertes_page() -> None:
    def content() -> None:
        ui.add_head_html('''
        <style>
            .pm-alerts-intro {
                color: #9ca4ae;
                font-size: .92rem;
                margin-top: -4px;
                margin-bottom: 8px;
            }
            .pm-alerts-stack {
                display: flex;
                flex-direction: column;
                gap: 14px;
                margin-top: 10px;
            }
            .pm-alert-card {
                background: #fbfbfb;
                border-radius: 18px;
                padding: 16px;
                box-shadow: inset 0 0 0 1px rgba(0,0,0,.03);
            }
            .pm-alert-head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                margin-bottom: 10px;
            }
            .pm-alert-title {
                color: #3f4854;
                font-size: 1rem;
                font-weight: 700;
                line-height: 1.2;
            }
            .pm-alert-text {
                color: #6a7380;
                font-size: .92rem;
                line-height: 1.45;
                margin-bottom: 10px;
            }
            .pm-alert-meta {
                color: #adb4bc;
                font-size: .82rem;
            }
            .pm-section-label {
                color: #434c57;
                font-size: 1rem;
                font-weight: 700;
                margin-top: 8px;
                margin-bottom: 2px;
                text-align: left;
            }
        </style>
        ''')

        ui.label('Surveillez les événements critiques, techniques et capteurs.').classes('pm-alerts-intro')

        with ui.element('div').classes('pm-alerts-stack'):
            with ui.element('div').classes('pm-alert-card'):
                with ui.element('div').classes('pm-alert-head'):
                    ui.label('Capteur CO₂ - Valeur anormale').classes('pm-alert-title')
                    render_alert_badge('Critique', 'danger')
                ui.label('Le capteur du salon remonte une valeur supérieure au seuil configuré.').classes('pm-alert-text')
                ui.label('Salon • Il y a 2 min').classes('pm-alert-meta')

            with ui.element('div').classes('pm-alert-card'):
                with ui.element('div').classes('pm-alert-head'):
                    ui.label('Connexion API instable').classes('pm-alert-title')
                    render_alert_badge('Warning', 'warning')
                ui.label('Certaines remontées de mesures ont été retardées sur les 10 dernières minutes.').classes('pm-alert-text')
                ui.label('Passerelle locale • Il y a 12 min').classes('pm-alert-meta')

            with ui.element('div').classes('pm-alert-card'):
                with ui.element('div').classes('pm-alert-head'):
                    ui.label('Synchronisation rétablie').classes('pm-alert-title')
                    render_alert_badge('Info', 'info')
                ui.label('Le service météo est de nouveau synchronisé avec le moteur de décision.').classes('pm-alert-text')
                ui.label('Cloud • Aujourd’hui').classes('pm-alert-meta')

        ui.label('Résumé rapide').classes('pm-section-label')
        render_stat_card(
            'Alertes du jour',
            [
                ('Critiques', '02'),
                ('Warnings', '04'),
                ('Infos', '03'),
            ],
        )

    dashboard_layout(title='Alertes', content=content, show_back=True)