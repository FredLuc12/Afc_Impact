from nicegui import ui
from database import get_connection
from pages.connexion import user_session
from components.layout import create_dashboard_layout

def home_content():
    """Contenu page Home avec stats BDD."""
    with ui.column().classes('gap-8 w-full'):
        ui.label('Bienvenue dans votre dashboard SUIVI4K !').classes('text-3xl text-gray-700 font-light')
        
        # Stats BDD
        if not user_session['user_id']:
            nb_alertes_actives = 0
            alertes_aujourdhui = 0 
            statut_global = 'Non connecté'
        else:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                # Compteur alertes actives (non résolues)
                cursor.execute("SELECT COUNT(*) as count FROM alerts WHERE resolved = 0")
                nb_alertes_actives = cursor.fetchone()[0]
                
                # Statut global
                cursor.execute("""
                    SELECT COUNT(*) as total_alertes 
                    FROM alerts 
                    WHERE created_at > datetime('now', '-1 day')
                """)
                alertes_aujourdhui = cursor.fetchone()[0]
                
                conn.close()
            except:
                nb_alertes_actives = 0
                alertes_aujourdhui = 0
        
        # Cards rapides avec DONNÉES RÉELLES
        with ui.row().classes('gap-6 w-full'):
            # STATUT GLOBAL
            with ui.card().classes('flex-1 p-8 shadow-xl rounded-3xl'):
                ui.icon('dashboard', color='green').classes('text-5xl mx-auto mb-4')
                ui.label('Statut').classes('text-3xl font-bold text-center text-green-600')
                
                if nb_alertes_actives == 0:
                    ui.label('OK').classes('text-xl text-center text-green-800')
                else:
                    ui.label(f' {nb_alertes_actives} alerte(s) active(s)').classes('text-xl text-center text-orange-700')
            
            # ALERTES
            with ui.card().classes('flex-1 p-8 shadow-xl rounded-3xl'):
                ui.icon('notifications', color='orange').classes('text-5xl mx-auto mb-4')
                ui.label('Alertes').classes('text-3xl font-bold text-center text-orange-600')
                ui.label(f'{nb_alertes_actives} actif').classes('text-xl text-center text-orange-800')
            
            # ALERTES JOUR
            with ui.card().classes('flex-1 p-8 shadow-xl rounded-3xl'):
                ui.icon('today', color='blue').classes('text-5xl mx-auto mb-4')
                ui.label('Aujourd\'hui').classes('text-3xl font-bold text-center text-blue-600')
                ui.label(f'{alertes_aujourdhui} alertes').classes('text-xl text-center text-blue-800')

@ui.page('/dashboard/home')
def dashboard_home():
    ui.page_title('SUIVI4K - Accueil')
    create_dashboard_layout('Home', home_content)
