from nicegui import ui

from app.layouts.auth_layout import auth_layout
from app.components.forms import render_input_field
from app.components.action_button import render_action_button


def register_page() -> None:
    def content() -> None:
        ui.add_head_html('''
        <style>
            .pm-auth-title {
                font-size: 1.9rem;
                font-weight: 700;
                color: #3f4854;
                margin-top: 24px;
                margin-bottom: 24px;
                line-height: 1.15;
            }
            .pm-register-note {
                text-align: center;
                margin-top: 18px;
                color: #b1b7bf;
                font-size: .82rem;
            }
            .pm-register-note a {
                color: #ea6a73;
                text-decoration: none;
            }
        </style>
        ''')

        ui.icon('arrow_back').classes('text-[#ea6a73] text-2xl cursor-pointer mt-2').on('click', lambda: ui.navigate.to('/login'))
        ui.label('Créer un compte').classes('pm-auth-title')

        nom = render_input_field('Nom complet', 'Ton nom complet')
        email = render_input_field('Email', 'Ton adresse email')
        identifiant = render_input_field('Identifiant', 'Choisir un identifiant')
        password = render_input_field('Mot de passe', 'Créer un mot de passe', password=True)
        confirm = render_input_field('Confirmer', 'Confirmer le mot de passe', password=True)

        ui.element('div').style('height: 18px')
        render_action_button('Créer mon compte', on_click=lambda: ui.navigate.to('/dashboard'), color='green')

        ui.label('Déjà inscrit ? Retour à la connexion').classes('pm-register-note')

    auth_layout(content)