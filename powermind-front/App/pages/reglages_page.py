# app/pages/reglages_page.py
# NOTE BDD: cette page nécessite une table 'seuils' ou similaire pour persister.
# En attendant, les valeurs sont sauvegardées dans choix_auto comme référence de config.
# Ici on utilise Supabase directement via une table 'seuils' si elle existe,
# sinon on affiche un message clair.

from nicegui import ui

from app.core.notifications import notify_success, notify_error
from app.core.security import require_role
from app.core.session import SessionManager
from app.core.utils import parse_uuid
from app.layouts.dashboard_layout import dashboard_layout
from app.core.supabase_client import get_supabase_client


def reglages_page() -> None:

    def content() -> None:
        if not require_role('admin', 'technicien'):
            return

        installation_id = SessionManager.get_installation_id()

        ui.label("Définissez les seuils d'alerte de vos capteurs.").classes('text-[#9ca4ae] text-sm -mt-1')

        with ui.card().classes('w-full p-4'):
            ui.label('Seuils de température (°C)').classes('text-sm font-semibold mb-2')
            temp_min = ui.number('Température min', value=18, min=-10, max=30, step=0.5).classes('w-full')
            temp_max = ui.number('Température max', value=24, min=10, max=40, step=0.5).classes('w-full')

        ui.element('div').style('height: 8px')

        with ui.card().classes('w-full p-4'):
            ui.label('Seuil CO₂ (ppm)').classes('text-sm font-semibold mb-2')
            co2_max = ui.number('CO₂ max', value=1500, min=400, max=5000, step=100).classes('w-full')

        ui.element('div').style('height: 8px')

        with ui.card().classes('w-full p-4'):
            ui.label('Seuil humidité (%)').classes('text-sm font-semibold mb-2')
            hum_min = ui.number('Humidité min', value=30, min=0, max=100, step=5).classes('w-full')
            hum_max = ui.number('Humidité max', value=70, min=0, max=100, step=5).classes('w-full')

        ui.element('div').style('height: 12px')

        def save_seuils():
            try:
                supabase = get_supabase_client()
                payload = {
                    'installation_id': installation_id,
                    'temp_min': temp_min.value,
                    'temp_max': temp_max.value,
                    'co2_max': co2_max.value,
                    'hum_min': hum_min.value,
                    'hum_max': hum_max.value,
                }
                # Upsert si la table 'seuils' existe en BDD
                supabase.table('seuils').upsert(payload, on_conflict='installation_id').execute()
                notify_success('Seuils enregistrés avec succès.')
            except Exception as e:
                # Si la table n'existe pas encore, on le signale clairement
                notify_error(f'Erreur : {str(e)} — Vérifiez que la table "seuils" existe en BDD.')

        ui.button('Enregistrer les seuils', on_click=save_seuils).props('color=primary').classes('w-full')

    dashboard_layout(title='Paramétrer les seuils', content=content, show_back=True)
