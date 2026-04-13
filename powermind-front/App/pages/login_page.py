from nicegui import ui

from app.layouts.auth_layout import auth_layout
from app.components.forms import render_input_field
from app.components.action_button import render_action_button


def login_page() -> None:
    def content() -> None:
        ui.add_head_html('''
        <style>
            .pm-auth-title {
                font-size: 2rem;
                font-weight: 700;
                color: #3f4854;
                margin-top: 42px;
                margin-bottom: 30px;
            }
            .pm-auth-note {
                text-align: center;
                margin-top: 20px;
                color: #b1b7bf;
                font-size: .8rem;
            }
            .pm-auth-note a {
                color: #ea6a73;
                text-decoration: none;
            }
            .pm-auth-links {
                display: flex;
                justify-content: space-between;
                margin-top: 8px;
                font-size: .82rem;
            }
            .pm-auth-links a {
                color: #ea6a73;
                text-decoration: none;
            }
        </style>
        ''')

        ui.icon('arrow_back').classes('text-[#ea6a73] text-2xl cursor-pointer mt-2').on('click', lambda: ui.navigate.to('/'))
        ui.label('Connexion').classes('pm-auth-title')

        identifiant = render_input_field('Identifiant', 'Ton identifiant')
        mot_de_passe = render_input_field('Mot de passe', 'Ton mot de passe', password=True)

        with ui.element('div').classes('pm-auth-links'):
            ui.link('Créer un compte', '/register')
            ui.link('Mot de passe oublié', '/forgot-password')

        ui.element('div').style('height: 30px')
        render_action_button('S’identifier', on_click=lambda: ui.navigate.to('/dashboard'), color='coral')

        ui.label('Je veux revenir sur mon dashboard Dashboard').classes('pm-auth-note')

    auth_layout(content)