from nicegui import ui
from uuid import UUID

from app.layouts.dashboard_layout import dashboard_layout
from app.core.supabase_client import get_supabase_client
from app.core.utils import parse_uuid
from app.core.notifications import notify_warning
from app.core.security import require_same_installation
from app.core.session import SessionManager


MODE_LABELS = {
    'confort': 'Confort',
    'ecologique': 'Écologique',
    'economique': 'Économique',
}

MODE_COLORS = {
    'confort': 'green',
    'ecologique': 'green',
    'economique': 'orange',
}


def _row(label: str, value: str) -> None:
    with ui.row().classes('w-full items-center justify-between no-wrap'):
        ui.label(label).classes('text-gray-500 shrink-0')
        ui.badge(str(value)).props('outline').classes('font-semibold shrink-0')


def _consigne_style(label: str):
    label_l = label.lower()

    if "température" in label_l:
        return "🌡️", "gray"
    if "co2" in label_l or "co₂" in label_l:
        return "🌫️", "gray"
    if "humidité" in label_l:
        return "💧", "gray"
    if "synchro" in label_l:
        return "🔄", "gray"
    if "chaudière" in label_l:
        return "🔥", "gray"
    if "source" in label_l:
        return "⚡", "gray"

    return "⚙️", "gray"


def _mode_card(mode: str, items: list[dict]) -> None:
    color = MODE_COLORS.get(mode, 'gray')

    with ui.card().classes(
        'w-full p-4 shadow-md rounded-xl'
    ).style(f'border-left: 6px solid {color}'):

        for c in items:
            _row("Température", c.get("temp_importance", "—"))
            _row("CO₂", c.get("co2_importance", "—"))
            _row("Humidité", c.get("humidity_importance", "—"))
            _row("Présence", c.get("pir_importance", "—"))

            ui.separator()

            with ui.row().classes('w-full justify-between items-center'):
                ui.label("Date").classes('text-gray-400 text-xs')
                ui.label(
                    c.get("created_at", "")[:16] if c.get("created_at") else "—"
                ).classes('text-gray-400 text-xs')


def valeurs_bases_page(installation_id: str | UUID | None = None) -> None:
    supabase = get_supabase_client()

    def content() -> None:
        current_installation_id = installation_id or SessionManager.get_installation_id()
        installation_uuid = parse_uuid(current_installation_id)

        if installation_uuid is None:
            notify_warning("Aucune installation valide n'est sélectionnée.")
            ui.label("Aucune installation sélectionnée.").classes("text-red-500")
            return

        if not require_same_installation(str(installation_uuid)):
            return

        response = (
            supabase
            .table("choix_auto")
            .select("*")
            .eq("installation_id", str(installation_uuid))
            .order("created_at", desc=False)
            .execute()
        )

        data = response.data or []

        if not data:
            ui.label("Aucune configuration automatique").classes("text-red-500")
            return

        # =========================
        # TABS
        # =========================
        with ui.tabs().classes("w-full") as tabs:
            tab1 = ui.tab('Configuration IA')
            tab2 = ui.tab('Informations')

        with ui.tab_panels(tabs, value=tab1).classes("w-full"):

            # =========================
            # TAB 1
            # =========================
            with ui.tab_panel(tab1):

                ui.label("Poids des facteurs IA").classes("text-2xl font-bold mb-2")

                grouped = {}
                for c in data:
                    grouped.setdefault(c.get("choix", "inconnu"), []).append(c)

                with ui.column().classes("w-full gap-4"):
                    for mode, items in grouped.items():
                        _mode_card(mode, items)

                ui.label("Consignes système").classes('text-xl font-bold mt-6 mb-3')

                consignes = [
                    ('Température économique', '18°C'),
                    ('Température absence', '16°C'),
                    ('Humidité confort', '40% – 60%'),
                    ('Seuil CO₂ alerte', '1000 ppm'),
                ]

                with ui.grid(columns=2).classes("w-full gap-2"):
                    for label, value in consignes:
                        icon, color = _consigne_style(label)

                        with ui.card().classes(
                            "p-2 rounded-lg shadow-sm hover:shadow transition"
                        ).style(f'border-left: 4px solid {color}'):

                            with ui.row().classes("items-center gap-2"):
                                ui.label(icon).classes("text-base")
                                ui.label(label).classes("text-gray-500 text-xs font-medium")

                            ui.label(value).classes("text-sm font-semibold mt-1")

            # =========================
            # TAB 2
            # =========================
            with ui.tab_panel(tab2):

                ui.label("Informations générales").classes("text-2xl font-bold mb-4")

                with ui.column().classes("w-full gap-3"):

                    with ui.card().classes("p-4 rounded-xl shadow-sm w-full h-28 flex flex-col justify-between"):
                        ui.label("État système").classes("font-bold")
                        ui.label("Tous les capteurs sont opérationnels").classes("text-sm text-gray-500")

                    with ui.card().classes("p-4 rounded-xl shadow-sm w-full h-28 flex flex-col justify-between"):
                        ui.label("Performance IA").classes("font-bold")
                        ui.label("Optimisation en temps réel active").classes("text-sm text-gray-500")

                    with ui.card().classes("p-4 rounded-xl shadow-sm w-full h-28 flex flex-col justify-between"):
                        ui.label("Dernière mise à jour").classes("font-bold")
                        ui.label("Synchronisé il y a 2 min").classes("text-sm text-gray-500")


    dashboard_layout(
        title='Configuration système automatique',
        content=content,
        show_back=True,
    )