from nicegui import ui

from app.layouts.dashboard_layout import dashboard_layout
from app.components.forms import render_input_field
from app.components.action_button import render_action_button
from app.components.filters import render_segmented_filter


def reglages_page() -> None:
    def content() -> None:
        render_segmented_filter(['Current Week', 'Last Month'], active='Last Month')
        render_input_field('Seuil température min', '18')
        render_input_field('Seuil température max', '24')
        render_input_field('Seuil CO₂', '1500')
        ui.element('div').style('height: 12px')
        render_action_button('Enregistrer', color='blue')

    dashboard_layout(title='Paramétrer les seuils', content=content, show_back=True)