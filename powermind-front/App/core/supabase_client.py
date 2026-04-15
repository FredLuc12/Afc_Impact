# app/core/supabase_client.py

import os
from functools import lru_cache
from dotenv import load_dotenv # 
from supabase import Client, create_client # 

# Charger les variables d'environnement au démarrage du module
load_dotenv() # 

class SupabaseConfigError(RuntimeError):
    """Erreur levée quand la configuration Supabase est absente ou invalide."""

def _clean_env(name: str) -> str:
    return (os.getenv(name) or '').strip() # 

def _get_supabase_settings() -> tuple[str, str]:
    url = _clean_env('SUPABASE_URL') # 
    
    # Priorité à la clé ANON pour le client public
    anon_key = _clean_env('SUPABASE_ANON_KEY') # 
    legacy_key = _clean_env('SUPABASE_KEY') # 
    
    key = anon_key or legacy_key

    if not url:
        raise SupabaseConfigError(
            "SUPABASE_URL manquant dans les variables d’environnement."
        )

    if not key:
        raise SupabaseConfigError(
            "SUPABASE_ANON_KEY (ou SUPABASE_KEY) manquant dans les variables d’environnement."
        )

    # Nettoyage de l'URL pour éviter les doubles slashs lors des appels API
    return url.rstrip('/'), key

@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """Instancie et met en cache le client Supabase."""
    url, key = _get_supabase_settings()
    return create_client(url, key) #

def is_supabase_configured() -> bool:
    """Vérifie si les clés nécessaires sont présentes pour l'authentification."""
    try:
        _get_supabase_settings()
        return True
    except SupabaseConfigError:
        return False