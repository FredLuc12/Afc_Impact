from nicegui import ui
from components.sidebar import render_sidebar

def create_dashboard_layout(title: str, content_func):
    """Layout avec sidebar (drawer) + contenu dynamique."""

    drawer = ui.left_drawer().classes('bg-white shadow-xl w-72')

    ui.button(
        '☰',
        on_click=lambda: drawer.toggle()
    ).classes(
        'fixed top-4 left-4 z-50 bg-white shadow-lg rounded-full w-12 h-12 text-xl'
    )

    with drawer:
        with ui.column().classes('p-6 gap-6 h-full'):
            render_sidebar(drawer)

    with ui.column().classes('p-6 pt-20 gap-8'):
        ui.label(title).classes('text-3xl font-bold text-gray-900')
        ui.separator().classes('w-full bg-gray-200')
        content_func()