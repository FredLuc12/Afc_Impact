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

        user    = getattr(response, 'user', None)
        session = getattr(response, 'session', None)

        if user:
            return {'success': True, 'message': 'Utilisateur créé.', 'user': user, 'session': session}
        return {'success': False, 'message': 'La création du compte a échoué.'}

    def login_user(self, identifier: str, password: str) -> dict:
        email    = (identifier or '').strip()
        password = password or ''

        if not email or not password:
            return {'success': False, 'message': 'Identifiants invalides.'}

        try:
            response = self.supabase.auth.sign_in_with_password({'email': email, 'password': password})
            user    = getattr(response, 'user', None)
            session = getattr(response, 'session', None)

            if not user:
                return {'success': False, 'message': 'Connexion impossible. Vérifiez vos identifiants.'}

            user_id = getattr(user, 'id', None)
            profile = {}
            installations = []

            if user_id:
                # 1. Profil
                profile_res = (
                    self.supabase.table('profiles')
                    .select('*')
                    .eq('id', user_id)
                    .maybe_single()
                    .execute()
                )
                profile = profile_res.data or {}
                role = profile.get('role', 'user')

                # 2. Installations
                if role in ['admin', 'super_admin']:
                    # Admin : toutes les installations (les 10 plus récentes)
                    inst_res = (
                        self.supabase.table('installations')
                        .select('*')
                        .order('created_at', desc=True)
                        .limit(10)
                        .execute()
                    )
                else:
                    # FIX CRITIQUE : on filtre par user_id (colonne profiles.id = installations.user_id)
                    # Si aucune installation trouvée → l'user n'en a pas encore (page d'attente)
                    inst_res = (
                        self.supabase.table('installations')
                        .select('*')
                        .eq('user_id', user_id)
                        .order('created_at', desc=True)
                        .execute()
                    )

                installations = inst_res.data or []

                # DEBUG : affiche en console pour vérifier
                print(f"[AUTH] user_id={user_id} | role={role} | installations trouvées={len(installations)}")

            default_installation = installations[0] if installations else {}

            return {
                'success': True,
                'message': 'Connexion réussie.',
                'user': {'id': user_id, 'email': getattr(user, 'email', email)},
                'session': session,
                'profile': profile,
                'installation': default_installation,
                'all_installations': installations,
            }

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'success': False, 'message': f'Erreur technique : {str(e)}'}
