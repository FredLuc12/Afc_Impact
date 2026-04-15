# app/services/auth_service.py

from app.core.supabase_client import get_supabase_client


class AuthService:
    def __init__(self) -> None:
        self.supabase = get_supabase_client()

    def register_user(self, email: str, password: str, full_name: str, username: str) -> dict:
        response = self.supabase.auth.sign_up({
            'email': email,
            'password': password,
            'options': {
                'data': {
                    'full_name': full_name,
                    'username': username,
                }
            },
        })

        user = getattr(response, 'user', None)
        session = getattr(response, 'session', None)

        if user:
            return {
                'success': True,
                'message': 'Utilisateur créé.',
                'user': user,
                'session': session,
            }

        return {
            'success': False,
            'message': 'La création du compte a échoué.',
        }

    def login_user(self, identifier: str, password: str) -> dict:
        email = (identifier or '').strip()
        password = password or ''

        if not email or not password:
            return {'success': False, 'message': 'Identifiants invalides.'}

        response = self.supabase.auth.sign_in_with_password({'email': email, 'password': password})
        user = getattr(response, 'user', None)
        session = getattr(response, 'session', None)

        if not user:
            return {'success': False, 'message': 'Connexion impossible. Vérifiez vos identifiants.'}

        user_id = getattr(user, 'id', None)
        profile = {}
        installation = {}

        if user_id:
            # Récupération du profil (role, full_name…)
            profile_res = (
                self.supabase.table('profiles')
                .select('*')
                .eq('id', user_id)
                .maybe_single()
                .execute()
            )
            profile = profile_res.data or {}

            # Récupération de la première installation de l'utilisateur
            inst_res = (
                self.supabase.table('installations')
                .select('*')
                .eq('user_id', user_id)
                .order('created_at', desc=True)
                .limit(1)
                .maybe_single()
                .execute()
            )
            installation = inst_res.data or {}

        return {
            'success': True,
            'message': 'Connexion réussie.',
            'user': {'id': user_id, 'email': getattr(user, 'email', email)},
            'session': session,
            'profile': profile,
            'installation': installation,
        }
