from nicegui import ui

from app.layouts.dashboard_layout import dashboard_layout
from app.components.alert_badge import render_alert_badge
from app.components.sensor_card import render_sensor_card


def valeurs_bases_page() -> None:
    def content() -> None:
        ui.add_head_html('''
        <style>
            .vb-title {
                color: #3f4854;
                font-size: 24px;
                font-weight: 700;
                margin-bottom: 6px;
            }
            .vb-subtitle {
                color: #9aa3ad;
                font-size: 13px;
                margin-bottom: 18px;
            }
            .vb-section-title {
                color: #3f4854;
                font-size: 16px;
                font-weight: 700;
                margin-top: 12px;
                margin-bottom: 10px;
            }
            .vb-panel {
                background: #ffffff;
                border-radius: 18px;
                padding: 16px;
                box-shadow: 0 10px 24px rgba(31, 41, 55, 0.06);
                border: 1px solid #eef1f4;
            }
            .vb-kpi-card {
                background: linear-gradient(180deg, #ffffff 0%, #fafbfc 100%);
                border-radius: 16px;
                padding: 14px;
                border: 1px solid #edf1f5;
                min-height: 88px;
            }
            .vb-kpi-label {
                color: #9ca4ae;
                font-size: 12px;
                margin-bottom: 8px;
            }
            .vb-kpi-value {
                color: #3f4854;
                font-size: 22px;
                font-weight: 700;
                line-height: 1.1;
            }
            .vb-kpi-note {
                color: #7dc86e;
                font-size: 12px;
                font-weight: 600;
                margin-top: 6px;
            }
            .vb-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 12px;
                padding: 10px 0;
                border-bottom: 1px solid #f0f2f5;
            }
            .vb-row:last-child {
                border-bottom: none;
            }
            .vb-row-label {
                color: #6b7280;
                font-size: 14px;
                font-weight: 500;
            }
            .vb-row-value {
                color: #3f4854;
                font-size: 14px;
                font-weight: 700;
            }
        </style>
        ''')

        ui.label('Valeurs de base').classes('vb-title')
        ui.label("Consignes, seuils et références du système PowerMind.").classes('vb-subtitle')

        ui.label('État général').classes('vb-section-title')
        with ui.row().classes('w-full').style('gap: 10px; flex-wrap: wrap;'):
            with ui.card().classes('vb-kpi-card').style('flex: 1; min-width: 150px;'):
                ui.label('Mode actif').classes('vb-kpi-label')
                ui.label('Automatique').classes('vb-kpi-value')
                ui.label('Priorité PAC').classes('vb-kpi-note')

            with ui.card().classes('vb-kpi-card').style('flex: 1; min-width: 150px;'):
                ui.label('Température cible').classes('vb-kpi-label')
                ui.label('21°C').classes('vb-kpi-value')
                ui.label('Confort standard').classes('vb-kpi-note')

        with ui.row().classes('w-full items-center').style('gap: 8px; margin-top: 14px; margin-bottom: 10px; flex-wrap: wrap;'):
            render_alert_badge('Capteurs synchronisés', 'success')
            render_alert_badge('CO₂ à surveiller', 'warning')
            render_alert_badge('Gaz en secours', 'info')

        ui.label('Consignes système').classes('vb-section-title')
        with ui.card().classes('vb-panel w-full'):
            rows = [
                ('Température économique', '18°C'),
                ('Température absence', '16°C'),
                ('Humidité confort', '40% - 60%'),
                ('Seuil CO₂ alerte', '1000 ppm'),
                ('Délai détection présence', '< 3 s'),
                ('Bascule chaudière gaz', 'Activée'),
                ('Source prioritaire', 'PAC'),
                ('Dernière synchronisation', 'Aujourd’hui à 14:20'),
            ]
            for label, value in rows:
                with ui.row().classes('vb-row w-full'):
                    ui.label(label).classes('vb-row-label')
                    ui.label(value).classes('vb-row-value')

        ui.label('Capteurs de référence').classes('vb-section-title')
        with ui.row().classes('w-full').style('gap: 12px; flex-wrap: wrap;'):
            render_sensor_card(
                title='Température intérieure',
                value='21.4°C',
                unit='Stable',
                status='online',
                icon='device_thermostat',
                color='green',
            )
            render_sensor_card(
                title='Température extérieure',
                value='12.8°C',
                unit='Météo locale',
                status='online',
                icon='wb_sunny',
                color='blue',
            )
            render_sensor_card(
                title='Humidité',
                value='48%',
                unit='Zone confort',
                status='online',
                icon='water_drop',
                color='cyan',
            )
            render_sensor_card(
                title='CO₂',
                value='920 ppm',
                unit='À surveiller',
                status='warning',
                icon='co2',
                color='orange',
            )
            render_sensor_card(
                title='Présence',
                value='Occupé',
                unit='Détection active',
                status='online',
                icon='motion_photos_on',
                color='purple',
            )
            render_sensor_card(
                title='Chaudière gaz',
                value='Secours prêt',
                unit='Standby',
                status='idle',
                icon='local_fire_department',
                color='red',
            )

        ui.label('Alertes et seuils').classes('vb-section-title')
        with ui.card().classes('vb-panel w-full'):
            with ui.row().classes('w-full items-center justify-between').style('margin-bottom: 10px;'):
                ui.label('État des alarmes').style('color:#3f4854;font-size:15px;font-weight:700;')
                render_alert_badge('1 alerte mineure', 'warning')

            rows = [
                ('CO₂ supérieur au niveau cible', 'Prévoir aération ou réduction occupation'),
                ('Aucune anomalie humidité', 'Valeur dans la plage recommandée'),
                ('Chaudière disponible en secours', 'Activation si rendement PAC insuffisant'),
            ]
            for title, desc in rows:
                with ui.column().classes('w-full').style('padding: 10px 0; border-bottom: 1px solid #f0f2f5;'):
                    ui.label(title).style('color:#3f4854;font-size:14px;font-weight:600;')
                    ui.label(desc).style('color:#97a0aa;font-size:12px;')
    dashboard_layout(
        title='Valeurs de base',
        content=content,
        show_back=True,
    )