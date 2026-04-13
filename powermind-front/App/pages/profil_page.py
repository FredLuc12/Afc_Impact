from nicegui import ui

from app.layouts.dashboard_layout import dashboard_layout
from app.components.forms import render_input_field
from app.components.action_button import render_action_button


def profil_page() -> None:
    def content() -> None:
        ui.label('Informations du compte utilisateur.').classes('text-[#9ca4ae] text-sm -mt-1 mb-3')
        render_input_field('Nom', 'Johanna Doe')
        render_input_field('Email', 'johanna@company.com')
        render_input_field('Rôle', 'Technicien')
        ui.element('div').style('height: 10px')
        render_action_button('Mettre à jour le profil', color='green')

    dashboard_layout(title='Profil', content=content, show_back=True)