from nicegui import ui
from uuid import UUID
from app.layouts.dashboard_layout import dashboard_layout
from app.services.sensor_service import CapteurService
from app.models.capteur import CapteurUpdate, CapteurCreate

def admin_capteurs_page() -> None:
    service = CapteurService()

    def content() -> None:
        ui.label('Gestion du parc capteurs').classes('text-2xl font-bold text-slate-800')
        ui.label('Administration globale du matériel et des attributions.').classes('text-sm text-slate-400 mb-6')

        container = ui.column().classes('w-full gap-4')

        # --- LOGIQUE DE RÉCUPÉRATION DES DONNÉES ---
        def get_all_installations():
            """Récupère toutes les installations via self.client de BaseService."""
            try:
                # On utilise service.client défini dans ton BaseService
                res = service.client.table('installations').select('id, nom').execute()
                return {inst['id']: inst['nom'] for inst in res.data} if res.data else {}
            except Exception as e:
                print(f"Erreur installations: {e}")
                return {}

        def refresh_list():
            """Affiche TOUS les capteurs présents en base de données."""
            container.clear()
            # Utilise la méthode de jointure pour voir à quelle installation appartient chaque capteur
            capteurs = service.list_all_with_details()
            inst_options = get_all_installations()

            with container:
                if not capteurs:
                    ui.label("Aucun capteur enregistré en base de données.").classes('text-gray-400 text-center w-full py-10')
                
                for c in capteurs:
                    # Données issues de la jointure SQL (installations est un dict imbriqué)
                    inst_info = c.get('installations') or {}
                    inst_name = inst_info.get('nom', 'Non attribué')
                    is_active = c.get('is_active', True)

                    # Carte Capteur avec bordure dynamique selon l'état
                    with ui.card().classes(f'w-full p-4 border-l-4 {"border-blue-500" if is_active else "border-gray-300"} shadow-sm bg-white'):
                        with ui.row().classes('w-full items-center justify-between'):
                            with ui.column().classes('gap-0 flex-1'):
                                ui.label(f"{c['nom']}").classes('font-bold text-slate-700')
                                ui.label(f"📍 {inst_name}").classes('text-xs text-slate-500')
                                ui.label(f"Type: {c.get('type', 'N/A')}").classes('text-[10px] text-slate-400 uppercase')
                            
                            with ui.row().classes('items-center gap-3'):
                                # SWITCH D'ACTIVATION (EF14)
                                ui.switch(value=is_active,
                                          on_change=lambda e, cid=c['id']: service.toggle_activation(UUID(cid), e.value)) \
                                    .props('dense color=blue-6')

                                # BOUTON ÉDITION (Changer attribution ou nom)
                                ui.button(icon='edit', on_click=lambda _, curr=c: open_edit_dialog(curr)) \
                                    .props('flat round color=blue-6 size=sm').classes('bg-blue-50')
                                
                                # BOUTON SUPPRESSION (CRUD complet)
                                ui.button(icon='delete', on_click=lambda _, cid=c['id']: delete_capteur(cid)) \
                                    .props('flat round color=red-5 size=sm').classes('bg-red-50')

        # --- DIALOGUE DE GESTION (AJOUT / MODIFICATION) ---
        with ui.dialog() as edit_dialog, ui.card().classes('p-6 w-[380px] rounded-2xl bg-white'):
            dialog_title = ui.label('').classes('text-lg font-bold mb-4 text-slate-800')
            
            # Champs de saisie
            nom_in = ui.input('Nom du capteur').classes('w-full mb-2').props('outlined dense color=blue')
            type_in = ui.select(['meteo', 'interieur', 'securite'], label='Type de capteur').classes('w-full mb-2').props('outlined dense color=blue')
            inst_select = ui.select({}, label='Attribuer à l\'installation').classes('w-full').props('outlined dense color=blue')
            
            current_editing_id = {'value': None}

            async def save():
                try:
                    # On prépare les données (installation_id peut être None)
                    target_inst = UUID(inst_select.value) if inst_select.value else None
                    
                    if current_editing_id['value']:
                        # --- MODE MISE À JOUR ---
                        payload = CapteurUpdate(
                            nom=nom_in.value,
                            installation_id=target_inst,
                            type=type_in.value
                        )
                        service.update(UUID(current_editing_id['value']), payload)
                        msg = "Matériel mis à jour"
                    else:
                        # --- MODE CRÉATION MANUELLE ---
                        payload = CapteurCreate(
                            nom=nom_in.value,
                            installation_id=target_inst,
                            type=type_in.value
                        )
                        service.create(payload)
                        msg = "Nouveau matériel enregistré"
                    
                    ui.notify(msg, type='positive')
                    edit_dialog.close()
                    refresh_list()
                except Exception as e:
                    ui.notify(f"Erreur BDD : {e}", type='negative')

            with ui.row().classes('w-full mt-6 justify-end'):
                ui.button('ANNULER', on_click=edit_dialog.close).props('flat color=grey')
                ui.button('ENREGISTRER', on_click=save).classes('bg-blue-600 text-white font-bold').props('unelevated')

        def open_edit_dialog(capteur_data=None):
            # On rafraîchit les installations à chaque ouverture pour être à jour
            inst_options = get_all_installations()
            inst_select.options = inst_options
            
            if capteur_data:
                dialog_title.text = "Modifier le matériel"
                nom_in.value = capteur_data['nom']
                type_in.value = capteur_data.get('type', 'meteo')
                inst_select.value = str(capteur_data['installation_id']) if capteur_data['installation_id'] else None
                current_editing_id['value'] = str(capteur_data['id'])
            else:
                dialog_title.text = "Enregistrer un nouveau matériel"
                nom_in.value = ""
                type_in.value = 'meteo'
                inst_select.value = None
                current_editing_id['value'] = None
            
            edit_dialog.open()

        async def delete_capteur(cid):
            if await ui.dialog().confirm(f'Supprimer définitivement ce capteur ?'):
                try:
                    service.delete(UUID(cid))
                    ui.notify('Capteur retiré du parc')
                    refresh_list()
                except Exception as e:
                    ui.notify(f"Erreur : {e}", type='negative')

        # --- BOUTON D'ACTION PRINCIPAL ---
        ui.button('ENREGISTRER UN NOUVEAU MATÉRIEL', icon='add_circle', 
                  on_click=lambda: open_edit_dialog()) \
            .classes('w-full py-4 bg-blue-600 text-white font-bold mb-4 shadow-lg').props('unelevated')

        # Chargement initial
        refresh_list()

    dashboard_layout(title='Admin Matériel', content=content, show_back=True)