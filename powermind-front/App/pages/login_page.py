from nicegui import ui
from database import get_connection, hash_password

GREEN = '#27ae60'
RED = '#e74c3c'
GRAY = '#7f8c8d'

# État utilisateur GLOBAL (fonctionne partout)
user_session = {'user_id': None, 'user_name': ''}

@ui.page('/connexion')
def connexion_page():
    ui.page_title('SUIVI4K - Connexion')
    
    with ui.column().classes('min-h-screen items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50 py-12 px-8'):
        with ui.card().classes('w-full max-w-2xl p-12 shadow-2xl rounded-3xl border border-white/50 backdrop-blur-sm bg-white/90'):
            with ui.column().classes('gap-10 items-center w-full'):
                # Header
                with ui.column().classes('items-center gap-6 mb-8'):
                    ui.image('/assets/logo.png').classes('h-32 w-auto shadow-xl rounded-2xl')
                    ui.label('Connexion SUIVI4K').classes('text-5xl font-black text-gray-800 drop-shadow-lg')
                    ui.label('Accédez à votre tableau de bord sécurisé').classes('text-xl text-gray-500 font-light')
                
                # Formulaire
                with ui.column().classes('w-full max-w-md gap-6'):
                    email_input = ui.input(
                        'Email', 
                        placeholder='jean.dupont@example.com'
                    ).classes('w-full text-xl py-4').props('outlined rounded-xl dense')
                    
                    password_input = ui.input(
                        'Mot de passe', 
                        placeholder='••••••••••••',
                        password=True
                    ).classes('w-full text-xl py-4').props('outlined rounded-xl dense')
                
                # Bouton Login
                def login():
                    email = email_input.value.strip()
                    password = hash_password(password_input.value)
                    
                    if not email or not password_input.value:
                        ui.notify("Veuillez remplir tous les champs", color='negative')
                        return
                    
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute(
                            "SELECT id, nom, prenom, email FROM users WHERE email=? AND password_hash=?",
                            (email, password)
                        )
                        user = cursor.fetchone()
                        conn.close()
                        
                        if user:
                            #GLOBAL STATE (SIMPLE ET FONCTIONNEL)
                            user_session['user_id'] = user['id']
                            user_session['user_name'] = f"{user['prenom']} {user['nom']}"
                            ui.notify(f"Bienvenue {user['prenom']} {user['nom']}", color='positive', position='top')
                            ui.navigate.to('/dashboard')
                        else:
                            ui.notify("Email ou mot de passe incorrect", color='negative', position='top')
                    except Exception as e:
                        ui.notify(f"Erreur serveur : {str(e)}", color='negative')
                
                ui.button(
                    ' S\'IDENTIFIER',
                    on_click=login
                ).classes(
                    'w-full text-2xl py-6 font-bold shadow-2xl hover:shadow-3xl rounded-2xl h-16 mt-4 '
                    'bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white'
                )
                
                ui.label(
                    "Je souhaite créer un compte"
                ).classes('text-lg font-semibold hover:underline cursor-pointer mt-6 text-center').style(f'color: {GRAY}').on(
                    'click', lambda: ui.notify('Création de compte bientôt disponible !', position='top')
                )
