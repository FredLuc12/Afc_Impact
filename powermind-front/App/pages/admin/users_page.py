from nicegui import ui
from app.layouts.dashboard_layout import dashboard_layout
from app.services.admin_service import AdminService
from app.constants import ROUTE_DASHBOARD

def admin_users_page() -> None:
    service = AdminService()
    
    def content() -> None:
        ui.label('Gestion des Utilisateurs').classes('text-2xl font-bold mb-4')
        
        try:
            response = service.get_all_profiles()
            profiles = response.data or []
            
            # Définition des colonnes
            columns = [
                {'name': 'full_name', 'label': 'Nom complet', 'field': 'full_name', 'align': 'left'},
                {'name': 'email', 'label': 'Email', 'field': 'email', 'align': 'left'},
                {'name': 'role', 'label': 'Rôle', 'field': 'role'},
                {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'align': 'center'},
            ]
            
            # Création du tableau
            table = ui.table(columns=columns, rows=profiles, row_key='id').classes('w-full')
            
            # Ajout du bouton dans la colonne 'actions' via un slot NiceGUI
            table.add_slot('body-cell-actions', '''
                <q-td :props="props">
                    <q-btn flat round color="primary" icon="dashboard" @click="$parent.$emit('open_user_dash', props.row)">
                        <q-tooltip>Voir Dashboard</q-tooltip>
                    </q-btn>
                </q-td>
            ''')

            # Gestion de l'événement clic envoyé par le bouton Quasar
            table.on('open_user_dash', lambda msg: handle_open_dashboard(msg.args))
            
        except Exception as e:
            ui.notify(f"Erreur : {str(e)}", type='negative')

    def handle_open_dashboard(row_data):
        # On récupère l'ID de l'installation associée à cet utilisateur
        # Note : Il faut s'assurer que ton AdminService récupère aussi l'ID d'installation dans sa requête
        user_id = row_data.get('id')
        
        # Ici, une petite subtilité : comme un admin peut voir n'importe qui, 
        # on doit d'abord trouver l'ID d'installation de cet utilisateur précis
        ui.notify(f"Ouverture du dashboard de {row_data.get('full_name')}...", color='info')
        
        # Redirection vers la route dynamique
        # Si tu n'as pas l'ID d'installation dans row_data, il faudra faire un petit fetch
        ui.navigate.to(f"{ROUTE_DASHBOARD}/{user_id}")

    dashboard_layout(title='Administration Users', content=content, show_back=True)