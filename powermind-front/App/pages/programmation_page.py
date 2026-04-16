# app/pages/programmation_page.py
from nicegui import ui
from uuid import UUID
from app.layouts.dashboard_layout import dashboard_layout
from app.core.session import SessionManager
from app.services.programmation_service import ProgrammationService
from app.core.utils import parse_uuid

def programmation_page() -> None:
    service = ProgrammationService()
    # Récupération de l'ID d'installation depuis la session
    inst_id_str = SessionManager.get_installation_id()
    inst_id = parse_uuid(inst_id_str) if inst_id_str else None

    def content() -> None:
        if not inst_id:
            ui.label("Erreur : Aucune installation détectée.").classes('text-red-500 p-4')
            return

        # --- TITRE ET EN-TÊTE ---
        ui.label('Programmation d’absence').classes('text-2xl font-bold text-slate-800')
        ui.label('Optimisez votre consommation pendant vos déplacements.').classes('text-sm text-slate-400 -mt-2 mb-6')

        # --- CONTENEUR DE LA LISTE ---
        container = ui.column().classes('w-full gap-4')

        def refresh_list():
            """Recharge les données et reconstruit l'affichage de la liste."""
            container.clear()
            progs = service.list_by_installation(inst_id)
            
            with container:
                if not progs:
                    with ui.card().classes('w-full p-10 items-center bg-slate-50 border-dashed border-2 border-slate-200 shadow-none'):
                        ui.icon('event_busy', color='slate-300').classes('text-5xl mb-2')
                        ui.label('Aucune absence programmée').classes('text-slate-400 font-medium')
                else:
                    for p in progs:
                        with ui.card().classes('w-full p-4 border-l-4 border-coral shadow-sm bg-white'):
                            with ui.row().classes('w-full items-center justify-between'):
                                with ui.column().classes('gap-0'):
                                    ui.label(p['label']).classes('font-bold text-slate-700')
                                    d_start = p['date_debut'][:10]
                                    d_end = p['date_fin'][:10]
                                    ui.label(f"Du {d_start} au {d_end}").classes('text-[11px] text-slate-400')
                                
                                with ui.row().classes('items-center gap-2'):
                                    # Badge avec couleur de fond pour lisibilité
                                    ui.badge(f"{p.get('temperature_cible', 16)}°C", color='blue-6').classes('px-2 py-1 text-white')
                                    # Bouton supprimer coloré en rouge
                                    ui.button(icon='delete', on_click=lambda _, pid=p['id']: delete_item(pid))\
                                        .props('flat round color=red-5 size=sm').classes('bg-red-50')

        async def delete_item(prog_id):
            try:
                service.delete(prog_id)
                ui.notify('Absence supprimée', type='info')
                refresh_list()
            except Exception as e:
                ui.notify(f"Erreur suppression : {e}", type='negative')

        # --- DIALOGUE D'AJOUT ---
        with ui.dialog() as dialog, ui.card().classes('p-6 w-[360px] rounded-2xl bg-white'):
            ui.label('Nouvelle période').classes('text-lg font-bold mb-4 text-slate-800')
            
            label_input = ui.input('Nom (ex: Vacances)').classes('w-full mb-2').props('outlined dense color=coral')
            with ui.row().classes('w-full gap-2'):
                start_input = ui.input('Début').classes('flex-1').props('type=date outlined dense color=coral')
                end_input = ui.input('Fin').classes('flex-1').props('type=date outlined dense color=coral')
            
            temp_input = ui.number('Température (°C)', value=16.0, format='%.1f').classes('w-full').props('outlined dense color=coral')
            
            async def save():
                print(f"Tentative d'insertion pour l'installation ID : {inst_id}") # DEBUG
                if not label_input.value or not start_input.value or not end_input.value:
                    ui.notify('Veuillez remplir tous les champs', type='warning')
                    return
                
                try:
                    service.insert(
                        installation_id=inst_id,
                        label=label_input.value,
                        date_debut=start_input.value,
                        date_fin=end_input.value,
                        temperature_cible=temp_input.value
                    )
                    ui.notify('Programmation ajoutée !', type='positive', icon='check_circle')
                    dialog.close()
                    label_input.value = start_input.value = end_input.value = ""
                    refresh_list()
                except Exception as e:
                    # Capture l'erreur RLS ici si non corrigée en SQL
                    ui.notify(f"Erreur : {e}", type='negative')

            # Bouton ENREGISTRER coloré en bleu pour contraster avec le Coral
            ui.button('ENREGISTRER', on_click=save).classes('w-full mt-4 py-2 text-white bg-blue-600 font-bold').props('unelevated')

        # --- BOUTON PRINCIPAL D'ACTION ---
        # Ajout d'une couleur de fond "Coral" explicite et texte blanc
        ui.button('PROGRAMMER UNE ABSENCE', icon='add', on_click=dialog.open)\
            .classes('w-full py-4 rounded-xl shadow-lg font-bold mt-2 text-white bg-[#ea6a73]')\
            .props('unelevated')

        ui.label('ABSENCES PRÉVUES').classes('text-xs font-bold uppercase text-slate-400 mt-8 mb-2')

        refresh_list()

    dashboard_layout(title='Planning', content=content, show_back=True)