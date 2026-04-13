from nicegui import ui
from components.layout import create_dashboard_layout
from datetime import datetime

def modif_content():
    """Contenu page Modifier Heure/Date."""
    with ui.row().classes('gap-3 w-full max-w-md mx-auto'):
        with ui.card().classes('p-3 shadow-md rounded-xl'):
            with ui.column().classes('gap-2'):
                # Date actuelle
                current_date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                ui.label(f'Date actuelle : {current_date}').classes(
                    'text-sm text-gray-500 p-1 bg-gray-50 rounded-lg'
                )

                with ui.row().classes('w-full gap-2'):
                    ui.date('Nouvelle date').classes('flex-1').props('outlined dense')
                    ui.time('Nouvelle heure').classes('flex-1').props('outlined dense')

                ui.button('Synchroniser', color='blue').classes(
                    'w-full text-sm py-1 px-2 rounded-lg shadow-sm'
                )

@ui.page('/modif')
def dashboard_modif():
    create_dashboard_layout(' Modifier Heure/Date', modif_content)