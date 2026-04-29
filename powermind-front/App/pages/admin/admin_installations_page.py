# app/pages/admin/admin_installations_page.py
from __future__ import annotations
from uuid import UUID

from nicegui import ui

from app.layouts.dashboard_layout import dashboard_layout
from app.services.installation_service import InstallationService
from app.services.capteur_service import CapteurService
from app.models.installation import InstallationCreate, InstallationUpdate
from app.models.capteur import CapteurCreate, CapteurUpdate


CAPTEUR_TYPES = ['meteo', 'interieur', 'securite', 'energie', 'autre']


def admin_installations_page() -> None:
    inst_svc    = InstallationService()
    capteur_svc = CapteurService()

    def content() -> None:
        ui.label('Gestion des installations').classes('text-2xl font-bold text-slate-800')
        ui.label('Créer, modifier, supprimer des installations et gérer leurs capteurs.') \
            .classes('text-sm text-slate-400 mb-6')

        list_container = ui.column().classes('w-full gap-4')

        # ── Refresh liste ─────────────────────────────────────────────────
        def refresh_list() -> None:
            list_container.clear()
            try:
                installations = inst_svc.list_all_with_details()
                users_lookup  = inst_svc.get_users_lookup()
            except Exception as e:
                ui.notify(f'Erreur chargement : {e}', type='negative')
                return

            with list_container:
                if not installations:
                    ui.label('Aucune installation enregistrée.') \
                        .classes('text-gray-400 text-center w-full py-10')
                    return

                for inst in installations:
                    iid = str(inst['id'])
                    nom        = inst.get('nom', '—')
                    user_id    = str(inst.get('user_id', ''))
                    user_email = users_lookup.get(user_id, user_id[:8] + '…')
                    capteurs   = inst.get('capteurs') or []

                    with ui.card().classes(
                        'w-full p-4 border-l-4 border-blue-500 shadow-sm bg-white'
                    ):
                        # En-tête installation
                        with ui.row().classes('w-full items-center justify-between'):
                            with ui.column().classes('gap-0 flex-1'):
                                ui.label(nom).classes('font-bold text-slate-700 text-base')
                                ui.label(f'👤 {user_email}').classes('text-xs text-slate-500')
                                ui.label(f'{len(capteurs)} capteur(s)') \
                                    .classes('text-[10px] text-slate-400 uppercase mt-1')

                            with ui.row().classes('items-center gap-2'):
                                ui.button(
                                    icon='edit',
                                    on_click=lambda _, i=inst: open_inst_dialog(i)
                                ).props('flat round color=blue-6 size=sm').classes('bg-blue-50')

                                ui.button(
                                    icon='delete',
                                    on_click=lambda _, i=iid: delete_installation(i)
                                ).props('flat round color=red-5 size=sm').classes('bg-red-50')

                        # Liste capteurs
                        if capteurs:
                            ui.separator().classes('my-2')
                            for cap in capteurs:
                                with ui.row().classes(
                                    'w-full items-center justify-between px-1 py-1'
                                ):
                                    with ui.row().classes('items-center gap-2'):
                                        ui.icon('sensors').classes('text-slate-400 text-sm')
                                        ui.label(cap.get('nom', '—')) \
                                            .classes('text-sm text-slate-600')
                                        ui.badge(cap.get('type', '—')) \
                                            .props('outline color=grey').classes('text-[10px]')

                                    with ui.row().classes('gap-1'):
                                        ui.button(
                                            icon='edit',
                                            on_click=lambda _, c=cap, i=iid: open_capteur_dialog(c, i)
                                        ).props('flat round color=blue size=xs')
                                        ui.button(
                                            icon='delete',
                                            on_click=lambda _, c=cap['id']: delete_capteur(c)
                                        ).props('flat round color=red size=xs')

                        ui.button(
                            'Ajouter un capteur', icon='add',
                            on_click=lambda _, i=iid: open_capteur_dialog(None, i)
                        ).props('flat color=blue size=sm').classes('mt-2')

        # ── Dialog installation ───────────────────────────────────────────
        with ui.dialog() as inst_dialog, ui.card().classes('p-6 w-[380px] rounded-2xl bg-white'):
            inst_dialog_title = ui.label('').classes('text-lg font-bold mb-4 text-slate-800')
            inst_nom_in   = ui.input('Nom de l\'installation').classes('w-full mb-2') \
                                .props('outlined dense color=blue')
            inst_user_sel = ui.select({}, label='Associer à un utilisateur').classes('w-full') \
                                .props('outlined dense color=blue')

            editing_inst: dict = {'id': None}

            def save_installation() -> None:
                nom  = (inst_nom_in.value or '').strip()
                u_id = inst_user_sel.value
                if not nom:
                    ui.notify('Le nom est obligatoire.', type='warning')
                    return
                if not u_id:
                    ui.notify('Veuillez sélectionner un utilisateur.', type='warning')
                    return
                try:
                    if editing_inst['id']:
                        inst_svc.update(
                            UUID(editing_inst['id']),
                            InstallationUpdate(nom=nom, user_id=UUID(u_id))
                        )
                        ui.notify('Installation mise à jour', type='positive')
                    else:
                        inst_svc.create(InstallationCreate(nom=nom, user_id=UUID(u_id)))
                        ui.notify('Installation créée', type='positive')
                    inst_dialog.close()
                    refresh_list()
                except Exception as e:
                    ui.notify(f'Erreur : {e}', type='negative')

            with ui.row().classes('w-full mt-6 justify-end gap-2'):
                ui.button('ANNULER', on_click=inst_dialog.close).props('flat color=grey')
                ui.button('ENREGISTRER', on_click=save_installation) \
                    .classes('bg-blue-600 text-white font-bold').props('unelevated')

        def open_inst_dialog(inst_data=None) -> None:
            inst_user_sel.options = inst_svc.get_users_lookup()
            if inst_data:
                inst_dialog_title.text = 'Modifier l\'installation'
                inst_nom_in.value      = inst_data.get('nom', '')
                inst_user_sel.value    = str(inst_data.get('user_id', ''))
                editing_inst['id']     = str(inst_data['id'])
            else:
                inst_dialog_title.text = 'Nouvelle installation'
                inst_nom_in.value      = ''
                inst_user_sel.value    = None
                editing_inst['id']     = None
            inst_dialog.open()

        def delete_installation(inst_id: str) -> None:
            try:
                inst_svc.delete(UUID(inst_id))
                ui.notify('Installation supprimée', type='positive')
                refresh_list()
            except Exception as e:
                ui.notify(f'Erreur suppression : {e}', type='negative')

        # ── Dialog capteur ────────────────────────────────────────────────
        with ui.dialog() as cap_dialog, ui.card().classes('p-6 w-[380px] rounded-2xl bg-white'):
            cap_dialog_title = ui.label('').classes('text-lg font-bold mb-4 text-slate-800')
            cap_nom_in  = ui.input('Nom du capteur').classes('w-full mb-2') \
                              .props('outlined dense color=blue')
            cap_type_in = ui.select(CAPTEUR_TYPES, label='Type').classes('w-full mb-2') \
                              .props('outlined dense color=blue')

            editing_cap: dict = {'id': None, 'installation_id': None}

            def save_capteur() -> None:
                nom  = (cap_nom_in.value or '').strip()
                typ  = cap_type_in.value
                i_id = str(editing_cap['installation_id'] or '')  # garanti string
                if not nom:
                    ui.notify('Le nom est obligatoire.', type='warning')
                    return
                if not typ:
                    ui.notify('Le type est obligatoire.', type='warning')
                    return
                if not i_id:
                    ui.notify('Installation manquante.', type='warning')
                    return

                try:
                    if editing_cap['id']:
                        capteur_svc.update(
                            UUID(str(editing_cap['id'])),
                            CapteurUpdate(nom=nom, type=typ)
                        )
                        ui.notify('Capteur mis à jour', type='positive')
                    else:
                        # On passe une string, pas un UUID object
                        capteur_svc.create(
                            CapteurCreate(nom=nom, type=typ, installation_id=i_id)
                        )
                        ui.notify('Capteur ajouté', type='positive')
                    cap_dialog.close()
                    refresh_list()
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    ui.notify(f'Erreur : {e}', type='negative')


            with ui.row().classes('w-full mt-6 justify-end gap-2'):
                ui.button('ANNULER', on_click=cap_dialog.close).props('flat color=grey')
                ui.button('ENREGISTRER', on_click=save_capteur) \
                    .classes('bg-blue-600 text-white font-bold').props('unelevated')

        def open_capteur_dialog(cap_data, installation_id: str) -> None:
            editing_cap['installation_id'] = installation_id
            if cap_data:
                cap_dialog_title.text = 'Modifier le capteur'
                cap_nom_in.value      = cap_data.get('nom', '')
                cap_type_in.value     = cap_data.get('type', CAPTEUR_TYPES[0])
                editing_cap['id']     = str(cap_data['id'])
            else:
                cap_dialog_title.text = 'Nouveau capteur'
                cap_nom_in.value      = ''
                cap_type_in.value     = CAPTEUR_TYPES[0]
                editing_cap['id']     = None
            cap_dialog.open()

        def delete_capteur(cap_id: str) -> None:
            try:
                capteur_svc.delete(UUID(cap_id))
                ui.notify('Capteur supprimé', type='positive')
                refresh_list()
            except Exception as e:
                ui.notify(f'Erreur suppression : {e}', type='negative')

        # ── Bouton principal + chargement initial ─────────────────────────
        ui.button(
            'CRÉER UNE NOUVELLE INSTALLATION', icon='add_circle',
            on_click=lambda: open_inst_dialog()
        ).classes('w-full py-4 bg-blue-600 text-white font-bold mb-4 shadow-lg') \
         .props('unelevated')

        refresh_list()

    dashboard_layout(title='Admin Installations', content=content, show_back=True)