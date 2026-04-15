from app.core.supabase_client import get_supabase_client

class AdminService:
    def __init__(self) -> None:
        self.supabase = get_supabase_client()

    def get_all_profiles(self):
        # On récupère le profil ET l'ID de la première installation associée
        return self.supabase.table('profiles').select('*, installations(id)').execute()