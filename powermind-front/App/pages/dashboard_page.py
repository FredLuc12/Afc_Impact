from __future__ import annotations
from uuid import UUID
from nicegui import ui
import os   
from app.core.notifications import notify_error, notify_warning
from app.core.security import require_same_installation
from app.core.session import SessionManager
from app.core.utils import parse_uuid
from app.core.supabase_client import get_supabase_client
from app.layouts.dashboard_layout import dashboard_layout
from app.services.dashboard_service import DashboardService
from app.services.mesure_service import MesureService
from src.Energy_Chooser.main import ia_energy_chooser

TYPE_CO2  = 1
TYPE_HUM  = 2
TYPE_TEMP = 3

def dashboard_page(installation_id: str | UUID | None = None) -> None:
    service    = DashboardService()
    mesure_svc = MesureService()


    def content() -> None:
        current_installation_id = installation_id or SessionManager.get_installation_id()
        installation_uuid = parse_uuid(current_installation_id)

        if installation_uuid is None:
            notify_warning("Aucune installation valide n'est sélectionnée.")
            ui.label('Aucune installation sélectionnée.').classes('text-red-500')
            return

        if not require_same_installation(str(installation_uuid)):
            return

        try:
            data = service.get_installation_overview(installation_uuid)
        except Exception as e:
            notify_error(f'Erreur chargement dashboard : {str(e)}')
            return

        capteurs = data.get('capteurs') or []
        alertes  = data.get('alertes') or []

        def format_for_model(data):
            mapping = {
                "temperature": "temp",
                "humidite": "humidity",
                "co2": "co2",
                "presence": "pir"
            }

            result = {}

            for row in data:
                code = row["code"]
                value = row["value"]

                if code not in mapping:
                    continue

                key = mapping[code]

                if key == "pir":
                    result[key] = bool(value) if value is not None else False
                else:
                    # autres valeurs numériques
                    result[key] = float(value) if value is not None else 0

            defaults = {
                "temp": 0,
                "humidity": 0,
                "co2": 0,
                "pir": False
            }

            for k, v in defaults.items():
                if k not in result:
                    result[k] = v

            return result

        def get_latest_measures():
            supabase = get_supabase_client()
            print(installation_uuid)
            response = supabase.rpc("get_latest_measures_by_installation", {
                 "installation_uuid": str(installation_uuid)
             }).execute()
            response = format_for_model(response.data)
            print(response)
            result, weights = ia_energy_chooser(response)
            print(result)
            print(weights)

            choix = "gaz" if result == 1 else "electric"

            insert_response = supabase.table("choix_auto").insert({
                "choix": choix,
                "installation_id": str(installation_uuid),

                "temp_importance": weights["temp"],
                "humidity_importance": weights["humidity"],
                "co2_importance": weights["co2"],
                "pir_importance": weights["pir"],
            }).execute()

            update_auto_ui(choix)
            return insert_response.data

        # ==========================
        # STATE
        # ==========================
        consigne_temp = {'value': 21}
        energie_mode  = {'value': 'electric'}

        # ==========================
        # TABS
        # ==========================
        with ui.tabs().classes('w-full') as tabs:
            tab_manuel = ui.tab('Manuel', icon='tune')
            tab_auto   = ui.tab('Automatique', icon='smart_toy')

        with ui.tab_panels(tabs, value=tab_manuel).classes('w-full'):

            # ======================================================
            # ONGLET MANUEL
            # ======================================================
            with ui.tab_panel(tab_manuel):

                # --- Controle température ---
                with ui.row().classes('w-full justify-center mt-4'):

                    with ui.column().classes('items-center gap-4'):

                        def increase():
                            consigne_temp['value'] += 1
                            temp_display.text = f"{consigne_temp['value']}°C"

                        def decrease():
                            consigne_temp['value'] -= 1
                            temp_display.text = f"{consigne_temp['value']}°C"

                    with ui.row().classes('items-center gap-4'):
                        ui.button('-', on_click=decrease).props('round color=red')
                        temp_display = ui.label(f"{consigne_temp['value']}°C").classes('text-3xl font-bold')
                        ui.button('+', on_click=increase).props('round color=green')

                # --- Choix énergie ---
                with ui.row().classes('w-full justify-center mt-6 items-center gap-4'):

                    def set_gaz():
                        energie_mode['value'] = 'gaz'

                    def set_elec():
                        energie_mode['value'] = 'electric'

                    def update_energy_buttons():
                        gaz_btn.props(f"color={'red' if energie_mode['value']=='gaz' else 'grey'}")
                        elec_btn.props(f"color={'green' if energie_mode['value']=='electric' else 'grey'}")

                def set_gaz():
                    energie_mode['value'] = 'gaz'
                    update_energy_buttons()

                def set_elec():
                    energie_mode['value'] = 'electric'
                    update_energy_buttons()

                with ui.row().classes('w-full justify-center mt-6'):
                        with ui.row().classes('items-center gap-4'):
                            gaz_btn = ui.button('Gaz', on_click=set_gaz).classes('w-32')
                            elec_btn = ui.button('Électrique', on_click=set_elec).classes('w-32')

                update_energy_buttons()

                ui.separator()

                # --- PARTIE COMMUNE ---
                render_common_section(mesure_svc, installation_uuid, capteurs)

            # ======================================================
            # ONGLET AUTO
            # ======================================================
            with ui.tab_panel(tab_auto):

                with ui.column().classes('items-center gap-3 mt-4 w-full'):

                    def update_auto_ui(choix: str):
                        gaz_btn_auto.props(f"color={'green' if choix == 'gaz' else 'grey'}")
                        elec_btn_auto.props(f"color={'green' if choix == 'electric' else 'grey'}")
                        ui.notify(f"Choix automatique activé 💡 : {choix }", color='purple')


                    def set_mode(mode):
                        if mode == 'eco':
                            gaz_btn_auto.props(f"color=grey")
                            elec_btn_auto.props(f"color=green")
                            ui.notify("Mode Économique activé 💡", color='green')

                        elif mode == 'confort':
                            gaz_btn_auto.props(f"color=green")
                            elec_btn_auto.props(f"color=grey")
                            ui.notify("Mode Confort activé 🔥", color='blue')
                        else:
                            gaz_btn_auto.props(f"color=grey")
                            elec_btn_auto.props(f"color=green")
                            ui.notify("Mode Écologique activé 🌱", color='teal')

                    def update_energy_buttons_auto():
                        gaz_btn_auto.props(f"color={'red' if energie_mode['value']=='gaz' else 'grey'}")
                        elec_btn_auto.props(f"color={'green' if energie_mode['value']=='electric' else 'grey'}")

                    ui.button('Déclencher choix auto', on_click=get_latest_measures).classes('w-64').props('color=purple')
                    ui.button('Économique', on_click=lambda: set_mode('eco')).classes('w-64').props('color=green')
                    ui.button('Confort', on_click=lambda: set_mode('confort')).classes('w-64').props('color=blue')
                    ui.button('Écologique', on_click=lambda: set_mode('ecologique')).classes('w-64').props('color=teal')

                    with ui.row().classes('w-full justify-center mt-6'):
                        with ui.row().classes('items-center gap-4'):
                            gaz_btn_auto = ui.button('Gaz').classes('w-32')
                            elec_btn_auto = ui.button('Électrique').classes('w-32')

                    update_energy_buttons_auto()

                ui.separator()

                # --- PARTIE COMMUNE ---
                render_common_section(mesure_svc, installation_uuid, capteurs)

    dashboard_layout(title='Dashboard', content=content, show_back=False)


# ==========================================================
# PARTIE COMMUNE FACTORISÉE
# ==========================================================

def render_common_section(mesure_svc, installation_uuid, capteurs):

    ui.label('Mesures actuelles').classes('text-sm font-semibold mt-2')

    with ui.row().classes('w-full gap-2 flex-wrap'):

        with ui.card().classes('p-3 flex-1 min-w-[100px] items-center'):
            ui.label('Température')
            temp_label = ui.label('—').classes('text-xl font-bold')

        with ui.card().classes('p-3 flex-1 min-w-[100px] items-center'):
            ui.label('Humidité')
            hum_label = ui.label('—').classes('text-xl font-bold')

        with ui.card().classes('p-3 flex-1 min-w-[100px] items-center'):
            ui.label('CO₂')
            co2_label = ui.label('—').classes('text-xl font-bold')

    def refresh():
        mesures = mesure_svc.list_by_installation(installation_uuid, limit=50)

        valeurs = {TYPE_TEMP: None, TYPE_HUM: None, TYPE_CO2: None}

        for m in mesures:
            tid = m.get('type_mesure_id')
            if tid in valeurs and valeurs[tid] is None:
                unite = (m.get('types_mesure') or {}).get('unite', '')
                val = m.get('value')
                if val is not None:
                    valeurs[tid] = f"{val} {unite}".strip()

        temp_label.text = valeurs[TYPE_TEMP] or '—'
        hum_label.text  = valeurs[TYPE_HUM]  or '—'
        co2_label.text  = valeurs[TYPE_CO2]  or '—'

    refresh()
    ui.timer(30.0, refresh)

    ui.separator()

    ui.label('Capteurs enregistrés').classes('text-sm font-semibold')

    if capteurs:
        for capteur in capteurs[:8]:
            with ui.row().classes('justify-between w-full'):
                ui.label(capteur.get('nom', 'Capteur'))
                ui.label(capteur.get('type', '—')).classes('text-xs text-gray-400')
    else:
        ui.label('Aucun capteur.')
