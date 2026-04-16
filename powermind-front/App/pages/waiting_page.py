# app/pages/waiting_page.py

from nicegui import ui
from app.layouts.auth_layout import auth_layout

def waiting_activation_page() -> None:
    def content() -> None:
        with ui.column().classes('w-full items-center justify-center q-pa-xl gap-6'):
            # Pastille visuelle
            with ui.element('div').classes('p-4 rounded-full bg-blue-50'):
                ui.icon('info', color='primary').classes('text-6xl')
            
            with ui.column().classes('items-center gap-2'):
                ui.label('Compte en attente de configuration').classes('text-2xl font-bold text-slate-800')
                ui.label('Votre accès au dashboard PowerMind n’est pas encore activé.').classes('text-slate-500 text-center')

            with ui.card().classes('bg-slate-50 p-6 border-none shadow-none rounded-2xl w-full max-w-md'):
                ui.label('Prochaine étape :').classes('text-xs font-bold uppercase text-slate-400 mb-2')
                ui.label('Contactez notre service commercial pour finaliser l’enregistrement de votre installation.').classes('text-sm text-slate-700 mb-4')
                
                with ui.row().classes('items-center gap-3 p-3 bg-white rounded-xl border border-slate-200'):
                    ui.icon('mail', color='primary')
                    ui.label('xxx@gmail.com').classes('font-medium text-slate-800')
            
            ui.button('Se déconnecter', on_click=lambda: ui.navigate.to('/logout')).props('flat color=grey')

    auth_layout(content)