from fastapi import FastAPI
from bdd.connexion import connexion
from main import ia_energy_chooser
from pydantic import BaseModel
from datetime import datetime
from typing import List
from supabase import create_client

app = FastAPI()
supabase = connexion()

class Choix_Auto_Output(BaseModel):
    id: int
    choix: str
    created_at: datetime
    

@app.post("/choix_auto",response_model=List[Choix_Auto_Output])
def choix_auto():
    print("route appelée")
    result = ia_energy_chooser()
    if result:
        result = "gaz"
    else:
        result = "electric"
    response = supabase.table("choix_auto").insert(
        {
        "choix": result
        }
    ).execute()

    return response.data
