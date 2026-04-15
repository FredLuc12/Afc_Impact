from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

def connexion():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if url is None or key is None:
        raise Exception(f"Value Missing : {url}, {key}")
    supabase = create_client(url, key)
    return supabase