from nicegui import ui

from app.layouts.dashboard_layout import dashboard_layout
from app.components.action_button import render_action_button
from app.components.alert_badge import render_alert_badge


def maintenance_page() -> None:
    def content() -> None:
        ui.label('Outils de maintenance et de supervision technique.').classes('text-[#9ca4ae] text-sm -mt-1')
        with ui.column().classes('gap-4 mt-3'):
            with ui.card().classes('w-full rounded-[18px] shadow-none bg-[#fbfbfb] p-4'):
                ui.label('État général du système').classes('text-[#3f4854] font-bold text-base')
                ui.element('div').style('height:8px')
                with ui.row().classes('gap-3 wrap'):
                    render_alert_badge('API OK', 'success')
                    render_alert_badge('MQTT Stable', 'info')
                    render_alert_badge('1 action requise', 'warning')
            render_action_button('Lancer un diagnostic', color='blue')
            render_action_button('Redémarrer les services', color='coral')

    dashboard_layout(title='Maintenance', content=content, show_back=True)