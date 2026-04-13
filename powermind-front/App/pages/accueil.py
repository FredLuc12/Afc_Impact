from nicegui import ui
from config.settings import GREEN, RED, GRAY

def accueil_page():
    """Page d'accueil SUIVI4K - Plein écran + 3 capteurs."""
    ui.page_title('SUIVI4K - Accueil')
    # Layout PLEIN ÉCRAN (enlève max-w-md)
    with ui.column().classes('w-screen h-screen items-center justify-center gap-12 p-8 bg-gradient-to-br from-gray-50 to-blue-50'):
        # Logo + titre (centré haut)
        with ui.column().classes('items-center gap-6'):
            ui.image('/static/logo.png').classes('h-64 w-auto shadow-2xl rounded-2xl')  # Plus grand
            ui.label('SUIVI4K').classes('text-7xl font-black text-gray-800 drop-shadow-2xl')  # ÉNORME

        # 3 CAPTEURS RÉELS (grille pleine largeur)
        with ui.row().classes('w-full max-w-6xl gap-8 px-12'):  # ← PLEIN ÉCRAN
            # DATE/HEURE
            with ui.card().classes('flex-1 p-8 bg-white shadow-2xl rounded-3xl text-center border-4 border-blue-100 hover:scale-105 transition-all'):
                ui.icon('schedule', color='blue').classes('text-6xl mx-auto mb-4')
                ui.label('26/02/2026').classes('text-4xl font-black text-gray-800')
                ui.label('11:30').classes('text-3xl text-gray-500 font-semibold')

            # TEMPÉRATURE & HUMIDITÉ
            with ui.card().classes('flex-1 p-8 bg-white shadow-2xl rounded-3xl text-center border-4 border-green-100 hover:scale-105 transition-all'):
                ui.icon('thermostat', color='green').classes('text-6xl mx-auto mb-4')
                ui.label('24°C / 65%').classes('text-4xl font-black text-green-700')
                ui.label('Temp & Humidité').classes('text-xl text-gray-600 uppercase tracking-wider')

            # MOUVEMENT
            with ui.card().classes('flex-1 p-8 bg-white shadow-2xl rounded-3xl text-center border-4 border-orange-100 hover:scale-105 transition-all'):
                ui.icon('motion_sensor_active', color='orange').classes('text-6xl mx-auto mb-4')
                ui.label('ACTIF').classes('text-4xl font-black text-orange-600')
                ui.label('Détecteur Mouvement').classes('text-xl text-gray-600 uppercase tracking-wider')

        # 3 BOUTONS GRANDS (pleine largeur)
        with ui.row().classes('w-full max-w-4xl gap-6 px-12'):
            ui.button(
                ' DÉMARRER',
                color=GREEN,
                on_click=lambda: ui.navigate.to('/connexion')
            ).classes('flex-1 text-2xl py-8 px-12 font-bold shadow-2xl hover:shadow-3xl rounded-3xl h-20')

            ui.button(
                ' PARAMÈTRES',
                color=GRAY,
                on_click=lambda: ui.navigate.to('/connexion')
            ).classes('flex-1 text-2xl py-8 px-12 font-bold shadow-2xl hover:shadow-3xl rounded-3xl h-20')

            ui.button(
                ' ALIMENTATION',
                color=RED,
                on_click=lambda: ui.navigate.to('/connexion')
            ).classes('flex-1 text-2xl py-8 px-12 font-bold shadow-2xl hover:shadow-3xl rounded-3xl h-20')

        # Lien création compte
        ui.link(' Créer un compte', target='/connexion').classes('text-xl font-semibold hover:underline mt-8').style(f'color: {GRAY}')

if __name__ == '__main__':
    accueil_page()
    ui.run()
