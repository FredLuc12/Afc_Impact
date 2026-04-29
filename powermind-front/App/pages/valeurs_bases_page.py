# app/pages/valeurs_bases_page.py
from __future__ import annotations

from uuid import UUID

from nicegui import ui

from app.layouts.dashboard_layout import dashboard_layout
from app.core.utils import parse_uuid
from app.core.notifications import notify_warning
from app.core.security import require_same_installation
from app.core.session import SessionManager
from app.services.choix_auto_service import ChoixAutoService


MODE_COLORS = {
    'confort':    '#22c55e',
    'ecologique': '#14b8a6',
    'economique': '#f97316',
    'gaz':        '#ef4444',
    'electric':   '#3b82f6',
}

CONSIGNES_SYSTEME: list[tuple[str, str]] = [
    ('Température économique', '18°C'),
    ('Température absence',    '16°C'),
    ('Humidité confort',       '40% – 60%'),
    ('Seuil CO₂ alerte',       '1000 ppm'),
]

MODE_INFOS = [
    ('Mode économique actif',  'Réduction de la consommation énergétique'),
    ('Mode confort actif',     'Priorité au bien-être thermique'),
    ('Mode écologique actif',  "Réduction de l'empreinte carbone"),
]


def _consigne_style(label: str) -> tuple[str, str]:
    ll = label.lower()
    if 'température' in ll:              return '🌡️', 'gray'
    if 'co2' in ll or 'co₂' in ll:      return '🌫️', 'gray'
    if 'humidité' in ll:                 return '💧', 'gray'
    if 'synchro' in ll:                  return '🔄', 'gray'
    if 'chaudière' in ll:                return '🔥', 'gray'
    if 'source' in ll:                   return '⚡', 'gray'
    return '⚙️', 'gray'


def _row(label: str, value: str) -> None:
    with ui.row().classes('w-full items-center justify-between no-wrap'):
        ui.label(label).classes('text-gray-500 shrink-0')
        ui.badge(str(value)).props('outline').classes('font-semibold shrink-0')


def valeurs_bases_page(installation_id: str | UUID | None = None) -> None:
    svc = ChoixAutoService()

    def content() -> None:
        current_installation_id = installation_id or SessionManager.get_installation_id()
        installation_uuid = parse_uuid(current_installation_id)

        if installation_uuid is None:
            notify_warning("Aucune installation valide n'est sélectionnée.")
            ui.label("Aucune installation sélectionnée.").classes('text-red-500')
            return

        if not require_same_installation(str(installation_uuid)):
            return

        # ─── ChoixAuto via service ────────────────────────────────────────
        # get_by_installation() retourne ChoixAuto | None
        # Le modèle contient maintenant tous les champs BDD y compris *_importance
        choix = svc.get_by_installation(installation_uuid)

        if choix is None:
            ui.label("Aucune configuration automatique trouvée.").classes('text-red-500')
            return

        # ─── TABS ─────────────────────────────────────────────────────────
        with ui.tabs().classes('w-full') as tabs:
            tab1 = ui.tab('Configuration IA')
            tab2 = ui.tab('Informations')

        with ui.tab_panels(tabs, value=tab1).classes('w-full'):

            # ── TAB 1 : poids IA ──────────────────────────────────────────
            with ui.tab_panel(tab1):
                ui.label("Poids des facteurs IA").classes("text-2xl font-bold mb-2")

                color = MODE_COLORS.get(choix.choix, '#6b7280')

                with ui.card().classes('w-full p-4 shadow-md rounded-xl').style(
                    f'border-left: 6px solid {color}'
                ):
                    ui.label(f"Mode : {choix.choix.capitalize()}").classes('font-bold text-lg mb-2')

                    _row("Température",
                         f"{round(choix.temp_importance, 3)}" if choix.temp_importance is not None else "—")
                    _row("CO₂",
                         f"{round(choix.co2_importance, 3)}" if choix.co2_importance is not None else "—")
                    _row("Humidité",
                         f"{round(choix.humidity_importance, 3)}" if choix.humidity_importance is not None else "—")
                    _row("Présence (PIR)",
                         f"{round(choix.pir_importance, 3)}" if choix.pir_importance is not None else "—")

                    ui.separator()

                    created = choix.created_at
                    date_str = str(created)[:16] if created else "—"
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label("Dernière mise à jour").classes('text-gray-400 text-xs')
                        ui.label(date_str).classes('text-gray-400 text-xs')

                ui.label("Consignes système").classes('text-xl font-bold mt-6 mb-3')

                with ui.grid(columns=2).classes('w-full gap-2'):
                    for label, value in CONSIGNES_SYSTEME:
                        icon, color = _consigne_style(label)
                        with ui.card().classes(
                            'p-2 rounded-lg shadow-sm hover:shadow transition'
                        ).style('border-left: 4px solid gray'):
                            with ui.row().classes('items-center gap-2'):
                                ui.label(icon).classes('text-base')
                                ui.label(label).classes('text-gray-500 text-xs font-medium')
                            ui.label(value).classes('text-sm font-semibold mt-1')

            # ── TAB 2 : informations ──────────────────────────────────────
            with ui.tab_panel(tab2):
                ui.label("Informations générales").classes("text-2xl font-bold mb-4")

                with ui.column().classes('w-full gap-3'):
                    for title, desc in MODE_INFOS:
                        with ui.card().classes(
                            'p-4 rounded-xl shadow-sm w-full flex flex-col gap-1'
                        ):
                            ui.label(title).classes('font-bold')
                            ui.label(desc).classes('text-sm text-gray-500')

    dashboard_layout(
        title='Configuration système automatique',
        content=content,
        show_back=True,
    )