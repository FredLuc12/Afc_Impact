from nicegui import ui
from components.layout import create_dashboard_layout
from database import get_connection, hash_password
from pages.connexion import user_session

def profil_content():
    """Contenu page Modifier Profil avec BDD."""
    with ui.column().classes('gap-8 w-full max-w-2xl mx-auto'):
        
        # Vérif utilisateur connecté
        if not user_session['user_id']:
            ui.label('Veuillez vous connecter d\'abord').classes('text-2xl text-red-600 text-center p-8')
            return
        
        # CHARGEMENT DONNÉES BDD
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nom, prenom, email FROM users WHERE id=?", (user_session['user_id'],))
        user_data = cursor.fetchone()
        conn.close()
        
        if not user_data:
            ui.label(' Utilisateur introuvable').classes('text-2xl text-red-600 text-center p-8')
            return
        
        # Formulaire avec DONNÉES RÉELLES
        nom_input = ui.input('Nom', value=user_data['nom']).classes('w-full text-xl').props('outlined')
        prenom_input = ui.input('Prénom', value=user_data['prenom']).classes('w-full text-xl').props('outlined')
        email_input = ui.input('Email', value=user_data['email']).classes('w-full text-xl').props('outlined')
        
        nouveau_mdp = ui.input('Nouveau mot de passe (laissez vide pour garder)', password=True).classes('w-full text-xl').props('outlined')
        confirmer_mdp = ui.input('Confirmer mot de passe', password=True).classes('w-full text-xl').props('outlined')
        
        # Bouton Sauvegarder
        def save_profil():
            nom = nom_input.value.strip().upper()
            prenom = prenom_input.value.strip()
            email = email_input.value.strip().lower()
            new_password = nouveau_mdp.value
            
            # Validation
            if not all([nom, prenom, email]):
                ui.notify("Tous les champs sont obligatoires", color='negative')
                return
            
            if new_password:
                if len(new_password) < 6:
                    ui.notify("Mot de passe trop court (min 6 caractères)", color='negative')
                    return
                if new_password != confirmer_mdp.value:
                    ui.notify("Les mots de passe ne correspondent pas", color='negative')
                    return
                password_hash = hash_password(new_password)
            else:
                password_hash = None  # Garde ancien
            
            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                # UPDATE BDD
                if password_hash:
                    cursor.execute("""
                        UPDATE users SET nom=?, prenom=?, email=?, password_hash=? 
                        WHERE id=?
                    """, (nom, prenom, email, password_hash, user_session['user_id']))
                else:
                    cursor.execute("""
                        UPDATE users SET nom=?, prenom=?, email=? 
                        WHERE id=?
                    """, (nom, prenom, email, user_session['user_id']))
                
                rows_affected = cursor.rowcount
                conn.commit()
                conn.close()
                
                if rows_affected > 0:
                    # Met à jour session
                    user_session['user_name'] = f"{prenom} {nom}"
                    ui.notify(" Profil mis à jour avec succès !", color='positive', position='top')
                else:
                    ui.notify("Aucune modification détectée", color='negative')
                    
            except Exception as e:
                ui.notify(f"Erreur : {str(e)}", color='negative')
        
        ui.button(
            ' SAUVEGARDER',
            on_click=save_profil,
            color='green'
        ).classes('w-full text-xl py-4 rounded-2xl shadow-xl font-bold')
        
        ui.label(f"Connecté : {user_session['user_name']}").classes('text-lg text-gray-600 mt-4 text-center italic')

@ui.page('/dashboard/profil')
def dashboard_profil():
    ui.page_title('SUIVI4K - Profil')
    create_dashboard_layout(' Modifier Profil', profil_content)
