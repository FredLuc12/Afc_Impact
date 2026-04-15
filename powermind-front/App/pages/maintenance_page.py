# app/pages/maintenance_page.py

from nicegui import ui

from app.core.notifications import notify_success, notify_error, notify_warning
from app.core.security import require_role
from app.core.session import SessionManager
from app.layouts.dashboard_layout import dashboard_layout
from app.services.capteur_service import CapteurService
from app.services.alerte_service import AlerteService
from app.core.utils import parse_uuid


def maintenance_page() -> None:

    def content() -> None:
        if not require_role('admin', 'technicien'):
            return

        installation_id = parse_uuid(SessionManager.get_installation_id())
        capteur_service = CapteurService()
        alerte_service = AlerteService()

        ui.label('Outils de maintenance et de supervision technique.').classes('text-[#9ca4ae] text-sm -mt-1')

        # --- État du système ---
        with ui.card().classes('w-full p-4 mb-3'):
            ui.label('État général du système').classes('text-sm font-semibold mb-3')

            try:
                capteurs = capteur_service.list_by_installation(installation_id) if installation_id else []
                alertes = alerte_service.list_by_installation(installation_id) if installation_id else []
                nb_capteurs = len(capteurs)
                nb_alertes = len(alertes)

                with ui.row().classes('gap-3 flex-wrap'):
                    with ui.chip(f'{nb_capteurs} capteur(s)', icon='sensors').props('color=positive outline'):
                        pass
                    if nb_alertes > 0:
                        with ui.chip(f'{nb_alertes} alerte(s)', icon='warning').props('color=warning outline'):
                            pass
                    else:
                        with ui.chip('Aucune alerte', icon='check_circle').props('color=positive outline'):
                            pass

            except Exception as e:
                ui.label(f'Impossible de récupérer l\'état : {str(e)}').classes('text-xs text-red-400')

        # --- Diagnostic ---
        with ui.card().classes('w-full p-4 mb-3'):
            ui.label('Diagnostic').classes('text-sm font-semibold mb-2')
            log_area = ui.textarea('Résultat').classes('w-full font-mono text-xs').props('readonly rows=5')

            def run_diagnostic():
                log_area.value = ''
                lines = ['=== Diagnostic PowerMind ===']
                try:
                    capteurs = capteur_service.list_by_installation(installation_id) if installation_id else []
                    lines.append(f'[OK] {len(capteurs)} capteur(s) trouvé(s)')
                    for c in capteurs:
                        lines.append(f'  → {c.nom} ({c.type})')
                except Exception as e:
                    lines.append(f'[ERR] Capteurs : {str(e)}')
                try:
                    alertes = alerte_service.list_by_installation(installation_id) if installation_id else []
                    lines.append(f'[OK] {len(alertes)} alerte(s) active(s)')
                except Exception as e:
                    lines.append(f'[ERR] Alertes : {str(e)}')
                lines.append('=== Fin du diagnostic ===')
                log_area.value = '\n'.join(lines)
                notify_success('Diagnostic terminé.')

            ui.button('Lancer le diagnostic', on_click=run_diagnostic).props('color=primary').classes('w-full mt-2')

        # --- Nettoyage alertes ---
        with ui.card().classes('w-full p-4'):
            ui.label('Actions').classes('text-sm font-semibold mb-2')

            def clear_alerts():
                if not installation_id:
                    notify_warning('Aucune installation sélectionnée.')
                    return
                try:
                    alertes = alerte_service.list_by_installation(installation_id)
                    for alerte in alertes:
                        alerte_service.delete(alerte.get('id'))
                    notify_success(f'{len(alertes)} alerte(s) supprimée(s).')
                except Exception as e:
                    notify_error(f'Erreur : {str(e)}')

            ui.button('Effacer toutes les alertes', on_click=clear_alerts).props('color=negative flat').classes('w-full')

    dashboard_layout(title='Maintenance', content=content, show_back=True)
