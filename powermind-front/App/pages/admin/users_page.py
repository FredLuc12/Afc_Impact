# app/pages/admin/users_page.py

from nicegui import ui
from app.layouts.dashboard_layout import dashboard_layout
from app.services.admin_service import AdminService
from app.services.installation_service import InstallationService
from app.constants import ROUTE_DASHBOARD


def admin_users_page() -> None:
    service = AdminService()
    install_service = InstallationService()

    def content() -> None:
        ui.label('Gestion des utilisateurs enregistrés.').classes('text-[#9ca4ae] text-sm -mt-1')

        try:
            response = service.get_all_profiles()
            profiles = response.data or []

            if not profiles:
                ui.label('Aucun utilisateur trouvé.').classes('text-sm text-gray-500 p-4')
                return

            columns = [
                {'name': 'role', 'label': 'Rôle', 'field': 'role', 'align': 'left'},
                {'name': 'id', 'label': 'ID', 'field': 'id', 'align': 'left'},
                {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'align': 'center'},
            ]

            table = ui.table(columns=columns, rows=profiles, row_key='id').classes('w-full')

            table.add_slot('body-cell-actions', '''
                <q-td :props="props">
                    <q-btn flat round color="primary" icon="dashboard"
                           @click="$parent.$emit('open_user_dash', props.row)">
                        <q-tooltip>Voir Dashboard</q-tooltip>
                    </q-btn>
                </q-td>
            ''')

            def handle_open_dashboard(msg):
                row_data = msg.args if hasattr(msg, 'args') else msg
                user_id = row_data.get('id')
                if not user_id:
                    ui.notify('ID utilisateur introuvable.', type='negative')
                    return
                # On cherche l'installation de cet utilisateur
                try:
                    installations = install_service.list_by_user(user_id)
                    if installations:
                        install_id = installations[0].id
                        ui.navigate.to(f'{ROUTE_DASHBOARD}/{install_id}')
                    else:
                        ui.notify(f'Aucune installation pour cet utilisateur.', type='warning')
                except Exception as e:
                    ui.notify(f'Erreur : {str(e)}', type='negative')

            table.on('open_user_dash', handle_open_dashboard)

        except Exception as e:
            ui.notify(f'Erreur chargement : {str(e)}', type='negative')

    dashboard_layout(title='Administration — Utilisateurs', content=content, show_back=True)
