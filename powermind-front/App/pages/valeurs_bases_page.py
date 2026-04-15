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
    
    # Récupération de l'ID installation depuis la session
    inst_id_str = SessionManager.get_installation_id()
    inst_id = UUID(inst_id_str) if inst_id_str else None

    def content() -> None:
        if not inst_id:
            ui.label("Erreur : Aucune installation détectée.").classes('text-red-500 p-4')
            return

        # --- RÉCUPÉRATION DES DONNÉES (BDD) ---
        # 1. Mode Actif
        latest_choix = choix_service.get_latest_by_installation(inst_id)
        current_mode = latest_choix.mode if latest_choix else "manuel"

        # 2. Capteurs de référence (Dernières mesures par type)
        # On récupère les mesures de l'installation (limitée aux plus récentes)
        recent_mesures = mesure_service.list_by_installation(inst_id, limit=20)
        
        # 3. Alertes
        alertes = alerte_service.list_by_installation(inst_id)

        # --- LOGIQUE FRONT-END ---
        async def toggle_mode(e):
            new_mode = "automatique" if e.value else "manuel"
            try:
                choix_service.create(ChoixAutoCreate(
                    installation_id=inst_id,
                    mode=new_mode
                ))
                ui.notify(f"Mode {new_mode} enregistré avec succès.", type='positive')
            except Exception as ex:
                ui.notify(f"Erreur lors de l'enregistrement : {str(ex)}", type='negative')

        ui.add_head_html('<style>...</style>') # Garder tes styles existants

        ui.label('Valeurs de base').classes('vb-title')
        ui.label("Consignes, seuils et références du système PowerMind.").classes('vb-subtitle')

        # --- SECTION : ÉTAT GÉNÉRAL (MODE) ---
        ui.label('Configuration du mode').classes('vb-section-title')
        with ui.row().classes('w-full').style('gap: 10px;'):
            with ui.card().classes('vb-kpi-card w-full'):
                with ui.row().classes('items-center justify-between w-full'):
                    with ui.column():
                        ui.label('Mode de pilotage').classes('vb-kpi-label')
                        ui.label('Actif').classes('vb-kpi-value')
                    # Switch pour gérer le mode Manuel/Auto
                    ui.switch('Mode Automatique', 
                              value=(current_mode == "automatique"), 
                              on_change=toggle_mode).props('color=coral')

        # --- SECTION : CAPTEURS DE RÉFÉRENCE (MESURES BDD) ---
        ui.label('Capteurs de référence').classes('vb-section-title')
        with ui.row().classes('w-full').style('gap: 12px; flex-wrap: wrap;'):
            
            # Fonction utilitaire pour extraire la dernière valeur d'un type spécifique
            def get_val(code):
                for m in recent_mesures:
                    if m.get('types_mesures', {}).get('code') == code:
                        return f"{m['valeur']}{m.get('types_mesures', {}).get('unite', '')}"
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
                status='warning' if '900' in get_val('CO2') else 'online',
                icon='co2',
                color='orange',
            )

        # --- SECTION : ALERTES ET SEUILS (ALERTS BDD) ---
        ui.label('Alertes et seuils').classes('vb-section-title')
        with ui.card().classes('vb-panel w-full'):
            with ui.row().classes('w-full items-center justify-between').style('margin-bottom: 10px;'):
                ui.label('Journal des anomalies').style('color:#3f4854;font-size:15px;font-weight:700;')
                nb_alertes = len([a for a in alertes if a.get('niveau') == 'critical'])
                render_alert_badge(f'{nb_alertes} critique(s)' if nb_alertes > 0 else 'Système sain', 
                                   'danger' if nb_alertes > 0 else 'success')

            if not alertes:
                ui.label("Aucune alerte en cours.").classes('text-gray-400 text-sm py-4 text-center')
            else:
                for alerte in alertes[:5]: # On affiche les 5 dernières
                    with ui.column().classes('w-full').style('padding: 10px 0; border-bottom: 1px solid #f0f2f5;'):
                        with ui.row().classes('w-full justify-between'):
                            ui.label(alerte.get('titre')).style('color:#3f4854;font-size:14px;font-weight:600;')
                            ui.label(alerte.get('created_at')).classes('text-[10px] text-gray-400')
                        ui.label(alerte.get('message')).style('color:#97a0aa;font-size:12px;')

    dashboard_layout(
        title='Valeurs de base',
        content=content,
        show_back=True,
    )