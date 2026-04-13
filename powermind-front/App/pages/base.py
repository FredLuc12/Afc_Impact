from nicegui import ui
from database import get_connection
from pages.connexion import user_session
from components.layout import create_dashboard_layout
from webhook import send_make_webhook

def insert_alerte(sensor_id, type_alerte, valeur, seuil, message):
    """Insère alerte BDD UNIQUEMENT (pas webhook)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alerts (sensor_data_id, type_alerte, message, sent)
            VALUES (?, ?, ?, 1)
        """, (sensor_id, type_alerte, message))
        conn.commit()
        conn.close()
    except:
        pass

def base_content():
    """Dashboard capteurs multi-salles + alertes."""
    with ui.column().classes('gap-6 w-full'):
        if not user_session['user_id']:
            ui.label('Connectez-vous pour voir vos données').classes(
                'text-xl text-red-600 text-center p-6')
            return
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Seuils
            cursor.execute("SELECT temp_max, humidite_max, mouvement_actif FROM thresholds WHERE id=1")
            seuils = cursor.fetchone()
            temp_max, humid_max, mouvement_actif = seuils or (28.0, 75.0, 1)
            
            # Dernières par salle
            cursor.execute("""
                SELECT s1.*
                FROM sensor_data s1
                INNER JOIN (
                    SELECT salle, MAX(created_at) as max_date
                    FROM sensor_data GROUP BY salle
                ) s2 ON s1.salle = s2.salle AND s1.created_at = s2.max_date
                ORDER BY created_at DESC
                LIMIT 3
            """)
            dernieres_donnees = cursor.fetchall()
            
            # 5 dernières alertes
            cursor.execute("SELECT type_alerte, message, created_at, resolved FROM alerts ORDER BY created_at DESC LIMIT 10")
            alertes_raw = cursor.fetchall()
            alertes = [dict(row) for row in alertes_raw]
            
            conn.close()
            
        except Exception as e:
            print("Erreur base_content:", e)
            temp_max, humid_max, mouvement_actif = (28.0, 75.0, 1)
            dernieres_donnees = []
            alertes = []
        
        # CAPTEURS PAR SALLE
        if not dernieres_donnees:
            ui.label("Aucune donnée capteur").classes("text-gray-500 text-center p-6 italic")
        else:
            for row in dernieres_donnees:
                salle = row["salle"]
                temp = row["temperature"]
                humid = row["humidite"]
                mouvement = row["mouvement"]
                timestamp = row["created_at"]
                sensor_id = row["id"]
                
                with ui.card().classes("p-6 shadow-xl rounded-2xl w-full border-2 border-gray-100"):
                    ui.label(f"SALLE : {salle.upper()}").classes("text-lg font-bold text-gray-700 mb-4")
                    
                    with ui.row().classes("gap-6 w-full"):
                        # TEMPÉRATURE
                        with ui.card().classes("flex-1 p-4 shadow rounded-xl border border-green-200"):
                            ui.label("TEMPÉRATURE").classes("text-sm font-bold text-green-700")
                            ui.label(f"{temp:.1f}°C").classes("text-2xl font-black text-green-600")
                            ui.label(f"Seuil: {temp_max}°C").classes("text-xs text-gray-500")
                            status = "OK" if temp <= temp_max else "ALERTE"
                            color = "text-green-700" if temp <= temp_max else "text-red-700"
                            ui.label(status).classes(f"text-sm font-semibold {color}")
                            
                            #ALERTE SEULEMENT BDD (pas webhook)
                            if temp > temp_max:
                                insert_alerte(sensor_id, "temperature", temp, temp_max, f"{salle}: {temp}°C > {temp_max}°C")
                        
                        # HUMIDITÉ
                        with ui.card().classes("flex-1 p-4 shadow rounded-xl border border-blue-200"):
                            ui.label("HUMIDITÉ").classes("text-sm font-bold text-blue-700")
                            ui.label(f"{humid:.0f}%").classes("text-2xl font-black text-blue-600")
                            ui.label(f"Seuil: {humid_max}%").classes("text-xs text-gray-500")
                            status = "OK" if humid <= humid_max else "ALERTE"
                            color = "text-blue-700" if humid <= humid_max else "text-red-700"
                            ui.label(status).classes(f"text-sm font-semibold {color}")
                            
                            #ALERTE SEULEMENT BDD (pas webhook)
                            if humid > humid_max:
                                insert_alerte(sensor_id, "humidite", humid, humid_max, f"{salle}: {humid}% > {humid_max}%")
                        
                        # MOUVEMENT
                        with ui.card().classes("flex-1 p-4 shadow rounded-xl border border-orange-200"):
                            ui.label("MOUVEMENT").classes("text-sm font-bold text-orange-700")
                            status_mvt = "ACTIF" if mouvement else "INACTIF"
                            ui.label(status_mvt).classes("text-2xl font-black text-orange-600")
                            ui.label(f"Dernière: {timestamp[:16]}").classes("text-xs text-gray-500")
                            if mouvement_actif:
                                ui.label("Surveillance active").classes("text-sm font-semibold text-orange-700")
        
        # TABLE ALERTES
        with ui.card().classes("p-6 shadow-xl rounded-2xl w-full"):
            ui.label("ALERTES RÉCENTES").classes("text-lg font-bold text-red-700 mb-4")
            ui.label(f"{len(alertes)} trouvées").classes("text-sm text-gray-500 mb-2")
            
            if not alertes:
                ui.label("Aucune alerte (testez ESP32 > seuils)").classes(
                    "text-gray-500 text-center py-6 italic")
            else:
                ui.table(
                    columns=[
                        {"name": "created_at", "label": "Date", "field": "created_at"},
                        {"name": "type_alerte", "label": "Type", "field": "type_alerte"},
                        {"name": "message", "label": "Message", "field": "message"},
                    ],
                    rows=[
                        {
                            "created_at": alerte["created_at"][:16] if alerte.get("created_at") else "N/A",
                            "type_alerte": alerte.get("type_alerte", "Inconnu"),
                            "message": alerte.get("message", "")[:50] + "..." if len(alerte.get("message", "")) > 50 else alerte.get("message", "")
                        }
                        for alerte in alertes
                    ]
                ).classes("w-full").props("dense striped")

@ui.page('/dashboard/base')
def dashboard_base():
    ui.page_title('SUIVI4K - Capteurs')
    create_dashboard_layout('Capteurs Multi-Salles', base_content)
