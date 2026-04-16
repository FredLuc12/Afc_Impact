# app/pages/forgot_password_page.py
# Réinitialisation de mot de passe via Supabase Auth (envoi d'un email magique)

from nicegui import ui

from app.core.notifications import notify_success, notify_error
from app.core.supabase_client import get_supabase_client, is_supabase_configured
from app.layouts.auth_layout import auth_layout


def forgot_password_page() -> None:

    def content() -> None:
        ui.add_head_html('''
        <style>
            .pm-auth-title {
                font-size: 2rem;
                font-weight: 700;
                color: #3f4854;
                margin-top: 32px;
                margin-bottom: 8px;
            }
            .pm-auth-sub {
                color: #9ca4ae;
                font-size: .88rem;
                margin-bottom: 28px;
                line-height: 1.5;
            }
            .pm-success-box {
                background: #f0fdf4;
                border: 1px solid #86efac;
                border-radius: 12px;
                padding: 16px;
                color: #166534;
                font-size: .9rem;
                line-height: 1.5;
                margin-top: 16px;
            }
        </style>
        ''')

        supabase_ready = is_supabase_configured()
        envoye = {'value': False}

        ui.icon('arrow_back').classes(
            'text-[#ea6a73] text-2xl cursor-pointer mt-2'
        ).on('click', lambda: ui.navigate.to('/login'))

        ui.label('Mot de passe oublié').classes('pm-auth-title')
        ui.label(
            'Saisissez votre adresse email. Vous recevrez un lien pour '
            'réinitialiser votre mot de passe.'
        ).classes('pm-auth-sub')

        email_input = ui.input(
            'Adresse email',
            placeholder='votre@email.com'
        ).classes('w-full').props('type=email')

        message_zone = ui.column().classes('w-full')

        def send_reset():
            if not supabase_ready:
                notify_error("Configuration Supabase absente.")
                return

            email = (email_input.value or '').strip().lower()
            if not email or '@' not in email:
                notify_error('Adresse email invalide.')
                return

            try:
                supabase = get_supabase_client()
                supabase.auth.reset_password_email(
                    email,
                    options={
                        # L'URL de redirection après clic dans l'email
                        # À adapter selon votre domaine de déploiement
                        'redirect_to': 'http://localhost:8080/reset-password'
                    }
                )
                envoye['value'] = True
                email_input.disable()
                message_zone.clear()
                with message_zone:
                    ui.html(
                        f'<div class="pm-success-box">'
                        f'✅ Un email a été envoyé à <strong>{email}</strong>.<br>'
                        f'Vérifiez votre boîte de réception (et vos spams).<br>'
                        f'Le lien expire dans 1 heure.'
                        f'</div>'
                    )
            except Exception as e:
                notify_error(f'Erreur lors de l\'envoi : {str(e)}')

        ui.element('div').style('height: 8px')

        btn = ui.button(
            'Envoyer le lien de réinitialisation',
            on_click=send_reset
        ).classes('w-full').props('color=coral')

        email_input.on('keydown.enter', lambda _: send_reset())

        message_zone  # affiché dynamiquement

        ui.element('div').style('height: 20px')
        with ui.row().classes('w-full justify-center gap-1'):
            ui.label('Vous vous souvenez ?').classes('text-sm text-gray-400')
            ui.link('Retour à la connexion', '/login').classes('text-sm text-[#ea6a73]')

    auth_layout(content)
