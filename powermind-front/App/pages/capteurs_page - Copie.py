from nicegui import ui

from app.layouts.dashboard_layout import dashboard_layout
from app.components.alert_badge import render_alert_badge
from app.components.stat_card import render_stat_card


def capteurs_page() -> None:
    def content() -> None:
        ui.label('État des capteurs connectés au logement.').classes('text-[#9ca4ae] text-sm -mt-1')
        render_stat_card('Capteurs actifs', [
            ('Température', 'OK'),
            ('Humidité', 'OK'),
            ('CO₂', 'Alerte'),
            ('Présence', 'OK'),
        ])
        ui.element('div').style('height: 12px')
        with ui.row().classes('gap-3 wrap'):
            render_alert_badge('Temp réel', 'success')
            render_alert_badge('1 anomalie', 'warning')
            render_alert_badge('Dernière sync 2 min', 'info')

    dashboard_layout(title='Capteurs', content=content, show_back=True)