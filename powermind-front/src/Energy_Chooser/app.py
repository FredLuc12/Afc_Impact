from fastapi import FastAPI
from bdd.connexion import connexion
from main import ia_energy_chooser
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()
supabase = connexion()

@app.post("/choix_auto")
def choix_auto(installation_uuid: str, data: dict):
    print("route appelée")
    result, weights = ia_energy_chooser(data)

    choix = "gaz" if result == 1 else "electric"

    response = supabase.table("choix_auto").insert({
        "choix": choix,
        "installation_id": installation_uuid,
        "temp_importance": weights["temp"],
        "humidity_importance": weights["humidity"],
        "co2_importance": weights["co2"],
        "pir_importance": weights["pir"],
    }).execute()

    return response.data
