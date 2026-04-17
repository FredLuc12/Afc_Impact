# app/pages/valeurs_bases_page.py
# CORRECTIONS :
# - update_usage_mode : synchrone (pas async) — FIX erreur 500
# - Valeurs toggle alignées sur la BDD ('electric' / 'gaz') via mapping
# - Logique intelligente : mode UI ↔ valeur BDD séparés
# - Affichage dynamique de la description sans rechargement

from nicegui import ui
from uuid import UUID

from app.layouts.dashboard_layout import dashboard_layout
from app.components.alert_badge import render_alert_badge
from app.components.sensor_card import render_sensor_card
from app.core.session import SessionManager
from app.services.mesure_service import MesureService
from app.services.alerte_service import AlerteService
from app.services.choix_auto_service import ChoixAutoService
from app.models.choix_auto import ChoixAutoCreate


# ── Mapping UI ↔ valeur réelle colonne 'choix' en BDD ─────────────
MODE_UI_TO_DB: dict[str, str] = {
    'confort':    'electric',
    'ecologique': 'electric',
    'economique': 'gaz',
}
MODE_DB_TO_UI: dict[str, str] = {
    'electric': 'confort',
    'gaz':      'economique',
}
MODE_DESCRIPTIONS: dict[str, str] = {
    'confort':    'Priorité au bien-être thermique. Le système choisit automatiquement la source la plus performante.',
    'ecologique': 'Priorité à la PAC (énergie propre). Bascule gaz uniquement si rendement insuffisant.',
    'economique': 'Optimisation tarifaire. La chaudière gaz est activée pendant les heures creuses pour réduire la facture.',
}

SENSOR_CARDS = [
    {'code': 'TEMP_INT', 'title': 'Température intérieure', 'icon': 'device_thermostat', 'color': 'green',  'unit_label': 'Référence BDD'},
    {'code': 'TEMP_EXT', 'title': 'Température extérieure', 'icon': 'wb_sunny',          'color': 'blue',   'unit_label': 'Météo locale'},
    {'code': 'HUM',      'title': 'Humidité',               'icon': 'water_drop',        'color': 'cyan',   'unit_label': 'Zone confort'},
    {'code': 'CO2',      'title': 'CO₂',                    'icon': 'co2',               'color': 'orange', 'unit_label': 'Dernière lecture'},
    {'code': 'PRESENCE', 'title': 'Présence',               'icon': 'motion_photos_on',  'color': 'purple', 'unit_label': 'Détection active'},
]


def valeurs_bases_page() -> None:
    mesure_service = MesureService()
    alerte_service = AlerteService()
    choix_service  = ChoixAutoService()

    inst_id_str = SessionManager.get_installation_id()
    inst_id = UUID(inst_id_str) if inst_id_str else None

    def content() -> None:
        if not inst_id:
            ui.label('Erreur : Aucune installation détectée.').classes('text-red-500 p-4')
            return

        # ── Chargement BDD ─────────────────────────────────────────
        latest_choix    = choix_service.get_latest()
        db_choix        = latest_choix.choix if latest_choix else 'electric'
        current_ui_mode = MODE_DB_TO_UI.get(db_choix, 'confort')
        recent_mesures  = mesure_service.list_by_installation(inst_id, limit=20)
        alertes         = alerte_service.list_by_installation(inst_id)

        def get_val(code: str) -> tuple[str, str]:
            for m in recent_mesures:
                tm = m.get('types_mesure') or {}
                if tm.get('code') == code:
                    return str(m.get('value', 'N/A')), tm.get('unite', '')
            return 'N/A', ''

        # ── FIX CRITIQUE : fonction SYNCHRONE (pas async) ──────────
        # async + ui.notify() sans contexte = erreur 500 NiceGUI
        def update_usage_mode(e) -> None:
            ui_mode = e.value
            db_val  = MODE_UI_TO_DB.get(ui_mode, 'electric')
            try:
                choix_service.create(ChoixAutoCreate(choix=db_val))
                desc_label.text = MODE_DESCRIPTIONS.get(ui_mode, '')
                db_label.text   = f'Valeur BDD enregistrée : « {db_val} »'
                ui.notify(f'Mode {ui_mode.upper()} activé.', type='positive', icon='check')
            except Exception as ex:
                ui.notify(f'Erreur enregistrement : {ex}', type='negative')

        # ── Styles (identiques à l'original) ───────────────────────
        ui.add_head_html('''
        <style>
            .vb-title         { color:#3f4854;font-size:24px;font-weight:700;margin-bottom:6px; }
            .vb-subtitle      { color:#9aa3ad;font-size:13px;margin-bottom:18px; }
            .vb-section-title { color:#3f4854;font-size:16px;font-weight:700;margin-top:12px;margin-bottom:10px; }
            .vb-panel         { background:#ffffff;border-radius:18px;padding:16px;
                                box-shadow:0 10px 24px rgba(31,41,55,.06);border:1px solid #eef1f4; }
            .vb-kpi-card      { background:linear-gradient(180deg,#ffffff 0%,#fafbfc 100%);
                                border-radius:16px;padding:14px;border:1px solid #edf1f5;min-height:88px; }
            .vb-kpi-label     { color:#9ca4ae;font-size:12px;margin-bottom:8px; }
            .vb-kpi-value     { color:#3f4854;font-size:22px;font-weight:700;line-height:1.1; }
            .vb-kpi-note      { color:#7dc86e;font-size:12px;font-weight:600;margin-top:6px; }
            .vb-row           { display:flex;justify-content:space-between;align-items:center;
                                gap:12px;padding:10px 0;border-bottom:1px solid #f0f2f5; }
            .vb-row:last-child { border-bottom:none; }
            .vb-row-label     { color:#6b7280;font-size:14px;font-weight:500; }
            .vb-row-value     { color:#3f4854;font-size:14px;font-weight:700; }
            .vb-db-hint       { color:#b0bac4;font-size:11px;font-style:italic;margin-top:4px; }
        </style>
        ''')

        ui.label('Valeurs de base').classes('vb-title')
        ui.label('Consignes, seuils et références du système PowerMind.').classes('vb-subtitle')

        # ── Mode de pilotage ───────────────────────────────────────
        ui.label('Mode de pilotage').classes('vb-section-title')
        with ui.card().classes('vb-panel w-full'):
            ui.label('Définissez la priorité du système :').classes('vb-kpi-label')
            ui.toggle(
                {'confort': 'Confort', 'ecologique': 'Écologique', 'economique': 'Économique'},
                value=current_ui_mode,
                on_change=update_usage_mode,
            ).props('unelevated color=primary')

            with ui.column().classes('mt-4 p-3 rounded-lg w-full').style('background:#f8fafc;'):
                ui.label('Description').classes('vb-kpi-label')
                desc_label = ui.label(MODE_DESCRIPTIONS.get(current_ui_mode, '')).classes('text-sm text-slate-600')
                db_label   = ui.label(f'Valeur BDD enregistrée : « {db_choix} »').classes('vb-db-hint')

        # ── État général ───────────────────────────────────────────
        ui.label('État général').classes('vb-section-title')
        with ui.row().classes('w-full').style('gap:10px;flex-wrap:wrap;'):
            with ui.card().classes('vb-kpi-card').style('flex:1;min-width:150px;'):
                ui.label('Mode actif').classes('vb-kpi-label')
                ui.label(current_ui_mode.capitalize()).classes('vb-kpi-value')
                render_alert_badge('Priorité PAC' if db_choix == 'electric' else 'Gaz activé', 'info')

            with ui.card().classes('vb-kpi-card').style('flex:1;min-width:150px;'):
                ui.label('Alertes actives').classes('vb-kpi-label')
                ui.label(str(len(alertes))).classes('vb-kpi-value')
                render_alert_badge('À traiter' if alertes else 'RAS', 'danger' if alertes else 'success')

        # ── Capteurs de référence ──────────────────────────────────
        ui.label('Capteurs de référence').classes('vb-section-title')
        with ui.row().classes('w-full').style('gap:12px;flex-wrap:wrap;'):
            for card in SENSOR_CARDS:
                val, unite = get_val(card['code'])
                is_warn = (
                    card['code'] == 'CO2'
                    and val != 'N/A'
                    and val.lstrip('-').isdigit()
                    and int(val) > 1000
                )
                render_sensor_card(
                    title=card['title'],
                    value=f'{val} {unite}'.strip() if val != 'N/A' else 'N/A',
                    unit=card['unit_label'],
                    status='warning' if is_warn else ('online' if val != 'N/A' else 'offline'),
                    icon=card['icon'],
                    color=card['color'],
                )

        # ── Consignes système ──────────────────────────────────────
        ui.label('Consignes système').classes('vb-section-title')
        with ui.card().classes('vb-panel w-full'):
            for label, value in [
                ('Température économique',    '18°C'),
                ('Température absence',       '16°C'),
                ('Humidité confort',          '40% – 60%'),
                ('Seuil CO₂ alerte',          '1000 ppm'),
                ('Délai détection présence',  '< 3 s'),
                ('Bascule chaudière gaz',     'Activée'),
                ('Source prioritaire',        'PAC'),
                ('Dernière synchronisation',  'Aujourd\'hui à 14:20'),
            ]:
                with ui.row().classes('vb-row w-full'):
                    ui.label(label).classes('vb-row-label')
                    ui.label(value).classes('vb-row-value')

        # ── Alertes ────────────────────────────────────────────────
        ui.label('Alertes et seuils').classes('vb-section-title')
        with ui.card().classes('vb-panel w-full'):
            with ui.row().classes('w-full items-center justify-between').style('margin-bottom:10px;'):
                ui.label('Journal des anomalies').style('color:#3f4854;font-size:15px;font-weight:700;')
                render_alert_badge(
                    f'{len(alertes)} alerte(s)' if alertes else 'Système sain',
                    'danger' if alertes else 'success',
                )

            if not alertes:
                ui.label('Aucune alerte en cours.').classes('text-gray-400 text-sm py-4 text-center w-full')
            else:
                for alerte in alertes[:5]:
                    cap_info = alerte.get('capteurs') or {}
                    with ui.column().classes('w-full').style('padding:10px 0;border-bottom:1px solid #f0f2f5;'):
                        with ui.row().classes('w-full items-center justify-between'):
                            ui.label(cap_info.get('nom', 'Capteur Système')).style(
                                'color:#3f4854;font-size:14px;font-weight:600;'
                            )
                            ui.label(str(alerte.get('created_at', '—'))).style(
                                'color:#adb4bc;font-size:11px;'
                            )
                        ui.label(alerte.get('message', 'Alerte sans description.')).style(
                            'color:#97a0aa;font-size:12px;'
                        )

    dashboard_layout(
        title='Valeurs de base',
        content=content,
        show_back=True,
    )
