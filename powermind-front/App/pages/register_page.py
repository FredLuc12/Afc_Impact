from nicegui import ui

from app.core.notifications import notify_error, notify_success
from app.layouts.auth_layout import auth_layout
from app.components.forms import render_input_field
from app.components.action_button import render_action_button
from app.services.auth_service import AuthService


def register_page() -> None:
    auth_service = AuthService()

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

        def handle_register() -> None:
            full_name = (nom.value or '').strip()
            user_email = (email.value or '').strip().lower()
            username = (identifiant.value or '').strip()
            user_password = password.value or ''
            confirm_password = confirm.value or ''

            if not full_name or not user_email or not username or not user_password or not confirm_password:
                notify_error('Merci de remplir tous les champs.')
                return

            if user_password != confirm_password:
                notify_error('Les mots de passe ne correspondent pas.')
                return

            if len(user_password) < 8:
                notify_error('Le mot de passe doit contenir au moins 8 caractères.')
                return

            try:
                result = auth_service.register_user(
                    email=user_email,
                    password=user_password,
                    full_name=full_name,
                    username=username,
                )

                if result.get('success'):
                    notify_success('Compte créé avec succès. Vérifie ton email si la confirmation est activée.')
                    ui.navigate.to('/login')
                    return

                notify_error(result.get('message', 'Inscription impossible.'))

            except Exception as e:
                notify_error(f'Erreur lors de la création du compte : {str(e)}')

        ui.icon('arrow_back').classes('text-[#ea6a73] text-2xl cursor-pointer mt-2').on(
            'click', lambda: ui.navigate.to('/login')
        )
        ui.label('Créer un compte').classes('pm-auth-title')

        nom = render_input_field('Nom complet', 'Ton nom complet')
        email = render_input_field('Email', 'Ton adresse email')
        identifiant = render_input_field('Identifiant', 'Choisir un identifiant')
        password = render_input_field('Mot de passe', 'Créer un mot de passe', password=True)
        confirm = render_input_field('Confirmer', 'Confirmer le mot de passe', password=True)

        ui.element('div').style('height: 18px')
        render_action_button('Créer mon compte', on_click=handle_register, color='green')

        with ui.row().classes('justify-center w-full mt-4'):
            ui.label('Déjà inscrit ? ').classes('pm-register-note')
            ui.link('Retour à la connexion', '/login').classes('pm-register-note')

    auth_layout(content)