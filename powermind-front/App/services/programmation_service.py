from uuid import UUID
from app.core.supabase_client import get_supabase_client

class ProgrammationService:
    def __init__(self) -> None:
        self.supabase = get_supabase_client()

    def list_by_installation(self, inst_id: UUID):
        return self.supabase.table('programmations') \
            .select('*') \
            .eq('installation_id', str(inst_id)) \
            .order('date_debut', desc=False) \
            .execute().data

    def create(self, data: dict):
        return self.supabase.table('programmations').insert(data).execute()

    def delete(self, prog_id: str):
        return self.supabase.table('programmations').delete().eq('id', prog_id).execute()
    
    def insert(self, installation_id: UUID, label: str, date_debut: str, date_fin: str, temperature_cible: float):
        data = {
            'installation_id': str(installation_id),
            'label': label,
            'date_debut': date_debut,
            'date_fin': date_fin,
            'temperature_cible': temperature_cible
        }
        return self.create(data)