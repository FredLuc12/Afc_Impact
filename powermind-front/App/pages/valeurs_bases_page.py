# # app/pages/valeurs_bases_page.py
# # CORRECTIONS BDD:
# # - choix_auto: colonne 'choix' (pas 'mode') + pas de FK installation_id
# # - mesures: colonne 'value' (pas 'valeur') + jointure 'types_mesure' (pas 'types_mesures')
# # - alertes: seulement 'message' (pas 'titre', 'niveau')
# # - ChoixAutoCreate: seulement champ 'choix' (pas installation_id/mode)

# from nicegui import ui
# from uuid import UUID
# from app.layouts.dashboard_layout import dashboard_layout
# from app.components.alert_badge import render_alert_badge
# from app.components.sensor_card import render_sensor_card
# from app.core.session import SessionManager
# from app.services.mesure_service import MesureService
# from app.services.alerte_service import AlerteService
# from app.services.choix_auto_service import ChoixAutoService
# from app.models.choix_auto import ChoixAutoCreate


# def valeurs_bases_page() -> None:
#     mesure_service = MesureService()
#     alerte_service = AlerteService()
#     choix_service = ChoixAutoService()

#     inst_id_str = SessionManager.get_installation_id()
#     inst_id = UUID(inst_id_str) if inst_id_str else None

#     def content() -> None:
#         if not inst_id:
#             ui.label("Erreur : Aucune installation détectée.").classes('text-red-500 p-4')
#             return

#         # 1. Dernier choix auto global (pas de FK installation_id en BDD)
#         latest_choix = choix_service.get_latest()
#         # Colonne réelle BDD: 'choix' (ex: 'electric', 'gaz')
#         current_mode = latest_choix.choix if latest_choix else "manuel"

#         # 2. Mesures récentes via jointure capteurs (pas de installation_id direct)
#         # list_by_installation retourne des dicts avec jointures
#         recent_mesures = mesure_service.list_by_installation(inst_id, limit=20)

#         # 3. Alertes via jointure capteurs
#         alertes = alerte_service.list_by_installation(inst_id)

#         async def toggle_mode(e):
#             new_choix = "electric" if e.value else "gaz"
#             try:
#                 # ChoixAutoCreate: seulement champ 'choix' en BDD
#                 choix_service.create(ChoixAutoCreate(choix=new_choix))
#                 ui.notify(f"Mode '{new_choix}' enregistré avec succès.", type='positive')
#             except Exception as ex:
#                 ui.notify(f"Erreur lors de l'enregistrement : {str(ex)}", type='negative')

#         ui.label('Valeurs de base').classes('text-xl font-bold')
#         ui.label("Consignes, seuils et références du système PowerMind.").classes('text-sm text-gray-500 -mt-1')

#         # --- MODE ---
#         ui.label('Configuration du mode').classes('text-base font-semibold mt-4')
#         with ui.card().classes('w-full p-4'):
#             with ui.row().classes('items-center justify-between w-full'):
#                 with ui.column():
#                     ui.label('Mode de pilotage').classes('text-xs text-gray-500')
#                     # Affiche la valeur réelle de la colonne 'choix'
#                     ui.label(current_mode.upper()).classes('text-lg font-bold')
#                 ui.switch(
#                     'Mode Électrique',
#                     value=(current_mode == "electric"),
#                     on_change=toggle_mode
#                 ).props('color=coral')

#         # --- CAPTEURS DE RÉFÉRENCE ---
#         ui.label('Capteurs de référence').classes('text-base font-semibold mt-4')
#         with ui.row().classes('w-full gap-3 flex-wrap'):

#             def get_val(code: str) -> str:
#                 """Extrait la dernière valeur pour un code de type_mesure donné."""
#                 for m in recent_mesures:
#                     # Jointure 'types_mesure' (sans 's' — nom réel de la table)
#                     tm = m.get('types_mesure') or {}
#                     if tm.get('code') == code:
#                         # Colonne 'value' (pas 'valeur')
#                         return f"{m.get('value', 'N/A')}{tm.get('unite', '')}"
#                 return "N/A"

#             render_sensor_card(
#                 title='Température intérieure',
#                 value=get_val('TEMP_INT'),
#                 unit='Référence BDD',
#                 status='online',
#                 icon='device_thermostat',
#                 color='green',
#             )
#             render_sensor_card(
#                 title='Humidité',
#                 value=get_val('HUM'),
#                 unit='Zone confort',
#                 status='online',
#                 icon='water_drop',
#                 color='cyan',
#             )
#             render_sensor_card(
#                 title='CO₂',
#                 value=get_val('CO2'),
#                 unit='Dernière lecture',
#                 status='warning' if 'N/A' not in get_val('CO2') else 'online',
#                 icon='co2',
#                 color='orange',
#             )

#         # --- ALERTES ---
#         ui.label('Alertes et seuils').classes('text-base font-semibold mt-4')
#         with ui.card().classes('w-full p-4'):
#             with ui.row().classes('w-full items-center justify-between mb-2'):
#                 ui.label('Journal des anomalies').classes('font-bold text-slate-700')
#                 render_alert_badge(
#                     f'{len(alertes)} alerte(s)' if alertes else 'Système sain',
#                     'danger' if alertes else 'success'
#                 )

#             if not alertes:
#                 ui.label("Aucune alerte en cours.").classes('text-gray-400 text-sm py-4 text-center')
#             else:
#                 for alerte in alertes[:5]:
#                     with ui.column().classes('w-full py-2 border-b border-gray-100'):
#                         with ui.row().classes('w-full justify-between'):
#                             capteur_info = alerte.get('capteurs') or {}
#                             ui.label(capteur_info.get('nom', 'Capteur inconnu')).classes('text-sm font-semibold text-slate-700')
#                             ui.label(str(alerte.get('created_at', '—'))).classes('text-[10px] text-gray-400')
#                         # Seul champ texte disponible: 'message'
#                         ui.label(alerte.get('message', '—')).classes('text-xs text-gray-500')

#     dashboard_layout(
#         title='Valeurs de base',
#         content=content,
#         show_back=True,
#     )

# app/pages/valeurs_bases_page.py
from nicegui import ui
from uuid import UUID
from app.layouts.dashboard_layout import dashboard_layout
from app.components.alert_badge import render_alert_badge
from app.components.sensor_card import render_sensor_card
from app.core.session import SessionManager
from app.services.mesure_service import MesureService
from app.services.alerte_service import AlerteService
from app.services.choix_auto_service import ChoixAutoService
from app.models.choix_auto import ChoixAutoCreate

def valeurs_bases_page() -> None:
    # Initialisation des services
    mesure_service = MesureService()
    alerte_service = AlerteService()
    choix_service = ChoixAutoService()

    # Récupération de l'ID d'installation en session
    inst_id_str = SessionManager.get_installation_id()
    inst_id = UUID(inst_id_str) if inst_id_str else None

    def content() -> None:
        if not inst_id:
            ui.label("Erreur : Aucune installation détectée.").classes('text-red-500 p-4')
            return

        # 1. RÉCUPÉRATION DES DONNÉES DEPUIS LA BDD
        # ----------------------------------------
        # Dernier choix auto global (Colonne réelle BDD: 'choix')
        latest_choix = choix_service.get_latest()
        current_mode = latest_choix.choix if latest_choix else "economique"

        # Mesures récentes via jointure capteurs (Colonne 'value')
        recent_mesures = mesure_service.list_by_installation(inst_id, limit=20)

        # Alertes via jointure capteurs
        alertes = alerte_service.list_by_installation(inst_id)

        # 2. LOGIQUE DES MODES D'USAGE (EF05)
        # -----------------------------------
        async def update_usage_mode(new_mode: str):
            try:
                # Création du choix (Modèle : seulement champ 'choix')
                choix_service.create(ChoixAutoCreate(choix=new_mode))
                ui.notify(f"Mode {new_mode.upper()} activé.", type='positive', icon='check')
                refresh_desc(new_mode)
            except Exception as ex:
                ui.notify(f"Erreur lors de l'enregistrement : {str(ex)}", type='negative')

        ui.label('Valeurs de base').classes('text-xl font-bold')
        ui.label("Consignes, seuils et références du système PowerMind.").classes('text-sm text-gray-500 -mt-1')

        # --- SECTION : MODES D'USAGE (EF05) ---
        ui.label('Modes d\'usage').classes('text-base font-semibold mt-4')
        with ui.card().classes('w-full p-4 border-none shadow-sm'):
            ui.label('Définissez la priorité du système :').classes('text-xs text-gray-400 mb-2')
            
            # Toggle boutons pour les 3 modes des spécifications
            mode_selector = ui.toggle({
                'confort': 'Confort', 
                'ecologique': 'Écologique', 
                'economique': 'Économique'
            }, value=current_mode, on_change=lambda e: update_usage_mode(e.value)).props('unelevated color=coral')

            with ui.column().classes('mt-4 p-3 bg-slate-50 rounded-lg w-full'):
                ui.label('Description :').classes('text-[10px] font-bold uppercase text-slate-400')
                description_label = ui.label('').classes('text-sm text-slate-600')

                def refresh_desc(mode_val):
                    descriptions = {
                        'confort': 'Priorité au bien-être thermique, sans contrainte énergétique forte.',
                        'ecologique': 'Priorité à la PAC et limitation des pics de consommation.',
                        'economique': 'Réduction et optimisation en fonction des périodes d’occupation.'
                    }
                    description_label.text = descriptions.get(mode_val, 'Mode personnalisé.')
                
                refresh_desc(current_mode)

        # --- SECTION : CAPTEURS DE RÉFÉRENCE ---
        ui.label('Capteurs de référence').classes('text-base font-semibold mt-4')
        with ui.row().classes('w-full gap-3 flex-wrap'):

            def get_val(code: str) -> str:
                """Extrait la valeur brute de la colonne 'value' via jointure 'types_mesure'."""
                for m in recent_mesures:
                    # Utilisation de 'types_mesure' au singulier selon ton schéma
                    tm = m.get('types_mesure') or {}
                    if tm.get('code') == code:
                        return f"{m.get('value', 'N/A')}{tm.get('unite', '')}"
                return "N/A"

            render_sensor_card(
                title='Température intérieure',
                value=get_val('TEMP_INT'),
                unit='Référence BDD',
                status='online',
                icon='device_thermostat',
                color='green',
            )
            render_sensor_card(
                title='Humidité',
                value=get_val('HUM'),
                unit='Zone confort',
                status='online',
                icon='water_drop',
                color='cyan',
            )
            render_sensor_card(
                title='CO₂',
                value=get_val('CO2'),
                unit='Dernière lecture',
                status='warning' if 'N/A' not in get_val('CO2') else 'online',
                icon='co2',
                color='orange',
            )

        # --- SECTION : ALERTES ---
        ui.label('Alertes et seuils').classes('text-base font-semibold mt-4')
        with ui.card().classes('w-full p-4 border-none shadow-sm'):
            with ui.row().classes('w-full items-center justify-between mb-2'):
                ui.label('Journal des anomalies').classes('font-bold text-slate-700')
                render_alert_badge(
                    f'{len(alertes)} alerte(s)' if alertes else 'Système sain',
                    'danger' if alertes else 'success'
                )

            if not alertes:
                ui.label("Aucune alerte en cours.").classes('text-gray-400 text-sm py-4 text-center')
            else:
                for alerte in alertes[:5]:
                    with ui.column().classes('w-full py-2 border-b border-gray-100 last:border-0'):
                        with ui.row().classes('w-full justify-between items-center'):
                            cap_info = alerte.get('capteurs') or {}
                            ui.label(cap_info.get('nom', 'Capteur Système')).classes('text-sm font-semibold text-slate-700')
                            ui.label(str(alerte.get('created_at', '—'))).classes('text-[10px] text-gray-400')
                        # Utilisation du champ 'message' uniquement (selon tes corrections BDD)
                        ui.label(alerte.get('message', 'Alerte sans description.')).classes('text-xs text-gray-500 italic')

    dashboard_layout(
        title='Valeurs de base',
        content=content,
        show_back=True,
    )