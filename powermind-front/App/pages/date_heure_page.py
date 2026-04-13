from datetime import datetime
from nicegui import ui


def date_heure_page() -> None:
    ui.add_head_html('''
    <style>
        .pm-screen {
            background: #f5f5f5;
            min-height: 100vh;
            padding: 20px 18px 28px 18px;
            font-family: Inter, Arial, sans-serif;
        }
        .pm-back {
            color: #ec6b73;
            font-size: 24px;
            font-weight: 500;
            line-height: 1;
            text-decoration: none;
        }
        .pm-title {
            color: #6a6f77;
            font-size: 19px;
            font-weight: 700;
            margin-top: 18px;
            margin-bottom: 24px;
        }
        .pm-section-top {
            border-top: 1px solid #e5e5e5;
            padding-top: 14px;
            margin-bottom: 14px;
        }
        .pm-title-line {
            width: 100px;
            height: 3px;
            background: #61666d;
            border-radius: 999px;
            margin-left: auto;
            margin-bottom: 12px;
        }
        .pm-picker-card {
            background: #ffffff;
            border-radius: 0;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,.06);
            border: 1px solid #ececec;
            margin-bottom: 26px;
        }
        .pm-picker-header {
            background: #6eaee4;
            color: white;
            text-align: center;
            padding: 14px 10px 8px 10px;
        }
        .pm-big-time {
            font-size: 34px;
            line-height: 1;
            font-weight: 300;
            letter-spacing: 1px;
        }
        .pm-picker-body {
            background: #fafafa;
            padding: 18px 14px 16px 14px;
        }
        .pm-clock-zone {
            position: relative;
            height: 150px;
            margin-bottom: 10px;
        }
        .pm-clock-face {
            width: 150px;
            height: 150px;
            background: #dbeaf7;
            border-radius: 999px 999px 0 0;
            margin: 0 auto;
            position: relative;
        }
        .pm-clock-center {
            width: 7px;
            height: 7px;
            background: #57a8df;
            border-radius: 999px;
            position: absolute;
            left: 50%;
            top: 92px;
            transform: translate(-50%, -50%);
        }
        .pm-clock-hand {
            width: 84px;
            height: 2px;
            background: #57a8df;
            position: absolute;
            left: 50%;
            top: 92px;
            transform-origin: 0% 50%;
            transform: rotate(0deg);
        }
        .pm-clock-tip {
            width: 18px;
            height: 18px;
            background: #57a8df;
            border-radius: 999px;
            position: absolute;
            right: -8px;
            top: -8px;
        }
        .pm-number {
            position: absolute;
            color: #6f747b;
            font-size: 16px;
            font-weight: 500;
        }
        .pm-confirm-text {
            color: #4d5258;
            font-size: 14px;
            margin-top: 10px;
            text-align: left;
        }
        .pm-actions {
            display: flex;
            justify-content: end;
            gap: 14px;
            padding-top: 12px;
        }
        .pm-cancel {
            color: #666;
            font-size: 13px;
            background: transparent;
            border: none;
        }
        .pm-ok {
            background: #5aa9e6;
            color: white;
            border: none;
            border-radius: 3px;
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 600;
        }
        .pm-dialog-card {
            min-width: 280px;
            max-width: 300px;
            padding: 18px 14px 10px 14px;
            border-radius: 4px;
            box-shadow: 0 14px 28px rgba(0,0,0,.28);
        }
        .pm-dialog-text {
            color: #4e535a;
            font-size: 15px;
            margin-bottom: 18px;
        }
    </style>
    ''')

    selected_date = {'value': datetime.now().strftime('%Y-%m-%d')}
    selected_time = {'value': '01:00'}

    with ui.dialog() as confirm_dialog, ui.card().classes('pm-dialog-card'):
        ui.label("Êtes vous sur d'enregistrer ?").classes('pm-dialog-text')
        with ui.row().classes('w-full justify-end items-center').style('gap: 12px;'):
            ui.button('CANCEL', on_click=confirm_dialog.close).props('flat').style(
                'color:#666;font-size:12px;font-weight:500;'
            )
            ui.button(
                'DISCARD',
                on_click=confirm_dialog.close,
            ).style(
                'background:#4da3e8;color:white;font-size:12px;font-weight:600;padding:6px 14px;border-radius:2px;'
            )

    def ask_save() -> None:
        confirm_dialog.open()

    with ui.column().classes('pm-screen w-full').style('max-width: 390px; margin: 0 auto;'):
        ui.link('←', '/home').classes('pm-back')
        ui.label('Modifier heure & date').classes('pm-title')

        with ui.column().classes('pm-section-top w-full'):
            ui.element('div').classes('pm-title-line')

            with ui.card().classes('pm-picker-card w-full').style('padding:0; border-radius:0;'):
                with ui.column().classes('w-full').style('gap:0;'):
                    with ui.element('div').classes('pm-picker-header'):
                        ui.label(selected_time['value']).classes('pm-big-time')
                        ui.label('1').style('font-size:13px; opacity:.85; margin-top:4px;')

                    with ui.element('div').classes('pm-picker-body'):
                        with ui.element('div').classes('pm-clock-zone'):
                            with ui.element('div').classes('pm-clock-face'):
                                ui.element('div').classes('pm-clock-center')
                                with ui.element('div').classes('pm-clock-hand'):
                                    ui.element('div').classes('pm-clock-tip')

                                ui.label('12').classes('pm-number').style('top:18px; left:50%; transform:translateX(-50%);')
                                ui.label('1').classes('pm-number').style('top:34px; right:38px;')
                                ui.label('2').classes('pm-number').style('top:66px; right:20px;')
                                ui.label('9').classes('pm-number').style('top:68px; left:20px;')
                                ui.label('10').classes('pm-number').style('top:36px; left:36px;')

                        ui.label("Réglez l'heure et la date de l'appareil.").style(
                            'color:#6a6f77; font-size:13px; margin-bottom:12px;'
                        )

                        time_input = ui.input('Heure', value=selected_time['value']).props('type=time').classes('w-full')
                        date_input = ui.input('Date', value=selected_date['value']).props('type=date').classes('w-full')

                        with ui.row().classes('w-full justify-end').style('gap: 10px; margin-top: 12px;'):
                            ui.button('CANCEL').props('flat').style('color:#666;')
                            ui.button('OK', on_click=ask_save).style(
                                'background:#5aa9e6;color:white;border-radius:2px;padding:6px 16px;'
                            )

            with ui.card().classes('pm-picker-card w-full').style('padding:0; opacity:.55; border-radius:0;'):
                with ui.column().classes('w-full').style('gap:0;'):
                    with ui.element('div').classes('pm-picker-header'):
                        ui.label('10').classes('pm-big-time')
                        ui.label('2025').style('font-size:13px; opacity:.85; margin-top:4px;')

                    with ui.element('div').classes('pm-picker-body'):
                        ui.date().props('minimal').classes('w-full')
                        with ui.row().classes('w-full justify-end').style('gap: 10px; margin-top: 10px;'):
                            ui.button('CANCEL').props('flat').style('color:#666;')
                            ui.button('OK').props('disable').style(
                                'background:#9fd0f5;color:white;border-radius:2px;padding:6px 16px;'
                            )