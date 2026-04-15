# app/pages/mesures_page.py

from nicegui import ui

from app.layouts.dashboard_layout import dashboard_layout
from app.services.mesure_service import MesureService


def mesures_page(installation_id) -> None:
    service = MesureService()

    def content() -> None:
        mesures = service.list_by_installation(installation_id)

        ui.label('Historique des mesures du logement.').classes('text-[#9ca4ae] text-sm -mt-1')

        with ui.card().classes('w-full p-4'):
            ui.label('Dernières mesures').classes('text-sm font-semibold mb-2')

            if mesures:
                for mesure in mesures[:20]:
                    capteur = mesure.get('capteurs') or {}
                    type_mesure = mesure.get('types_mesures') or {}
                    ui.label(
                        f"{capteur.get('nom', 'Capteur')} | {type_mesure.get('code', '—')} | {mesure.get('valeur', '—')} {type_mesure.get('unite', '')}"
                    ).classes('text-sm')
            else:
                ui.label('Aucune mesure disponible.').classes('text-sm text-gray-500')

    dashboard_layout(title='Mesures', content=content, show_back=True)