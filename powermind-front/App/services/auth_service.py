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

    # app/services/auth_service.py

    def login_user(self, identifier: str, password: str) -> dict:
        email = (identifier or '').strip()
        password = password or ''

        if not email or not password:
            return {'success': False, 'message': 'Identifiants invalides.'}

        try:
            response = self.supabase.auth.sign_in_with_password({'email': email, 'password': password})
            user = getattr(response, 'user', None)
            session = getattr(response, 'session', None)

            if not user:
                return {'success': False, 'message': 'Connexion impossible. Vérifiez vos identifiants.'}

            user_id = getattr(user, 'id', None)
            profile = {}
            installations = [] # On passe au pluriel pour gérer plusieurs sites

            if user_id:
                # 1. Récupération du profil
                profile_res = self.supabase.table('profiles').select('*').eq('id', user_id).maybe_single().execute()
                profile = profile_res.data or {}
                role = profile.get('role', 'user')

                # 2. Logique selon le rôle
                if role in ['admin', 'super_admin']:
                    # Un admin veut souvent voir la liste globale ou TOUTES les installations
                    # Pour l'instant, on récupère les dernières installations créées globalement
                    inst_res = self.supabase.table('installations').select('*').order('created_at', desc=True).limit(5).execute()
                    installations = inst_res.data or []
                else:
                    # Un utilisateur standard : on récupère SES installations uniquement
                    inst_res = self.supabase.table('installations').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
                    installations = inst_res.data or []

            # On renvoie la première installation comme "active" par défaut, ou None si vide
            default_installation = installations[0] if installations else {}

            return {
                'success': True,
                'message': 'Connexion réussie.',
                'user': {'id': user_id, 'email': getattr(user, 'email', email)},
                'session': session,
                'profile': profile,
                'installation': default_installation,
                'all_installations': installations # Utile pour un sélecteur de site
            }
        except Exception as e:
            return {'success': False, 'message': f'Erreur technique : {str(e)}'}
