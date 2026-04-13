from nicegui import ui

from app.layouts.dashboard_layout import dashboard_layout
from app.components.tables import render_simple_table


def installations_page() -> None:
    def content() -> None:
        ui.label('Liste des installations PowerMind suivies.').classes('text-[#9ca4ae] text-sm -mt-1')
        render_simple_table(
            'Installations',
            ['Nom', 'Ville', 'Statut'],
            [
                ['Résidence A', 'Paris', 'Active'],
                ['Appartement B', 'Créteil', 'Test'],
                ['Site pilote C', 'Lyon', 'Maintenance'],
            ],
        )

    dashboard_layout(title='Installations', content=content, show_back=True)