from nicegui import ui, app
from database import get_connection, create_tables
from webhook import send_make_webhook
import json
from fastapi import Request  # ← IMPORT CRUCIAL

# ===== ROUTE ESP32 SAID (GET racine) =====
@app.get('/')
async def api_esp32_said(request: Request):  # ← Request FastAPI
    """ESP32 Said → http://10.130.13.100/?data={JSON}"""
    try:
        # Récupère JSON depuis query params
        json_data = request.query_params.get('data', '{}')
        data = json.loads(json_data)
        
        if not data or 'salle1' not in data:
            return {'status': 'error', 'message': 'JSON invalide'}
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Seuils
        cursor.execute("SELECT temp_max, humidite_max FROM thresholds WHERE id=1")
        seuils = cursor.fetchone()
        temp_max, humid_max = seuils if seuils else (28.0, 75.0)
        
        # INSERT + CHECK ALERTES
        for salle, donnees in data.items():
            cursor.execute("""
                INSERT INTO sensor_data (temperature, humidite, mouvement, salle)
                VALUES (?, ?, ?, ?)
            """, (donnees['temp'], donnees['hum'], donnees['pir'], salle))
            
            # Alertes seuils
            if donnees['temp'] > temp_max:
                send_make_webhook("temperature", donnees['temp'], temp_max, f"{salle}: {donnees['temp']}°C")
            if donnees['hum'] > humid_max:
                send_make_webhook("humidite", donnees['hum'], humid_max, f"{salle}: {donnees['hum']}%")
        
        # Nettoyage 50 dernières
        cursor.execute("DELETE FROM sensor_data WHERE id NOT IN (SELECT id FROM sensor_data ORDER BY id DESC LIMIT 50)")
        conn.commit()
        conn.close()
        
        return {'status': 'ok', 'salles': list(data.keys())}
        
    except json.JSONDecodeError:
        return {'status': 'error', 'message': 'JSON malformé'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

create_tables()
app.add_static_files('/assets', 'static')

# Pages UI (GET uniquement)
from pages.accueil import accueil_page
from pages.connexion import connexion_page
from pages.home import dashboard_home
from pages.base import dashboard_base
from pages.modif import dashboard_modif
from pages.profil import dashboard_profil
from pages.dashboard import dashboard_page

# IMPORTANT : Page d'accueil APRÈS route API
ui.page('/dashboard')(dashboard_page)
ui.page('/connexion')(connexion_page)
ui.page('/home')(dashboard_home)
ui.page('/profil')(dashboard_profil)
ui.page('/modif')(dashboard_modif)
ui.page('/base')(dashboard_base)
ui.page('/')(accueil_page)  # ← Page accueil UI

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(host='127.0.0.1', port=8081, reload=True, show=True, title='SUIVI4K')