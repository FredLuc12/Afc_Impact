from nicegui import ui


def consommation_page() -> None:
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
            color: #3e4852;
            font-size: 21px;
            font-weight: 700;
            margin-top: 18px;
            margin-bottom: 24px;
        }
        .pm-ring-label {
            color: #b0b5bc;
            font-size: 12px;
        }
        .pm-ring-wrap {
            width: 96px;
            height: 96px;
            border-radius: 999px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: conic-gradient(var(--ring-color) calc(var(--value) * 1%), #e8e8e8 0);
            position: relative;
        }
        .pm-ring-wrap::after {
            content: '';
            position: absolute;
            inset: 6px;
            border-radius: 999px;
            background: #f5f5f5;
        }
        .pm-ring-value {
            position: relative;
            z-index: 1;
            font-size: 16px;
            font-weight: 700;
            color: var(--ring-color);
        }
        .pm-chart-card {
            background: #efefef;
            border-radius: 14px;
            padding: 16px 14px 14px 14px;
            margin-top: 10px;
        }
        .pm-bars {
            height: 92px;
            display: flex;
            align-items: end;
            gap: 9px;
        }
        .pm-bar {
            width: 8px;
            border-radius: 3px 3px 0 0;
            background: #8f9397;
        }
        .pm-bar.soft { background: #bebebe; }
        .pm-bar.red { background: #ee6f79; }
        .pm-bar.red-soft { background: #f49da4; }
        .pm-avatar {
            width: 28px;
            height: 28px;
            border-radius: 999px;
            object-fit: cover;
            background: #ddd;
        }
        .pm-market-name {
            color: #5d636a;
            font-size: 14px;
            font-weight: 500;
        }
        .pm-market-price {
            color: #9b9fa5;
            font-size: 13px;
            font-weight: 600;
        }
    </style>
    ''')

    with ui.column().classes('pm-screen w-full').style('max-width: 390px; margin: 0 auto;'):
        ui.link('←', '/home').classes('pm-back')
        ui.label('Consommation').classes('pm-title')

        with ui.row().classes('w-full justify-between items-start').style(
            'margin-top: 6px; border-top: 1px solid #e7e7e7; padding-top: 16px;'
        ):
            for label, value, color in [
                ('Consommation en cours', 64, '#72d7a0'),
                ('Consommation hier', 90, '#5f6ae9'),
            ]:
                with ui.column().classes('items-center').style('width: 46%; gap: 10px;'):
                    ui.label(label).classes('pm-ring-label')
                    with ui.element('div').classes('pm-ring-wrap').style(
                        f'--value:{value}; --ring-color:{color};'
                    ):
                        ui.label(f'{value}%').classes('pm-ring-value')

        with ui.column().classes('w-full').style('margin-top: 12px;'):
            with ui.row().classes('w-full items-end justify-between').style(
                'border-top: 1px solid #e7e7e7; padding-top: 12px;'
            ):
                ui.element('div')
                with ui.column().classes('items-end').style('gap: 6px;'):
                    ui.label('Optimisations des prospects').style(
                        'color:#3e4852;font-size:14px;font-weight:700;'
                    )
                    ui.element('div').style(
                        'width:104px;height:3px;background:#3e4852;border-radius:999px;'
                    )

            with ui.element('div').classes('pm-chart-card w-full'):
                with ui.row().classes('pm-bars w-full no-wrap').style('justify-content: space-between;'):
                    bars = [42, 50, 58, 34, 74, 55, 47, 59, 58, 30, 66, 44, 73, 41, 68, 35, 52]
                    styles = [
                        'soft', '', '', 'soft', '', 'soft', '', '', 'soft',
                        'red-soft', 'red', 'red-soft', 'red', 'red-soft', 'red', 'red-soft', 'red'
                    ]
                    for h, s in zip(bars, styles):
                        ui.element('div').classes(f'pm-bar {s}').style(f'height:{h}px;')

        with ui.column().classes('w-full').style('margin-top: 14px;'):
            with ui.row().classes('w-full items-end justify-between').style(
                'border-top: 1px solid #e7e7e7; padding-top: 12px;'
            ):
                ui.element('div')
                with ui.column().classes('items-end').style('gap: 6px;'):
                    ui.label('Tarifs du marché').style(
                        'color:#3e4852;font-size:14px;font-weight:700;'
                    )
                    ui.element('div').style(
                        'width:104px;height:3px;background:#3e4852;border-radius:999px;'
                    )

            data = [
                ('Gaz', '$1300.50', 'https://i.pravatar.cc/60?img=32'),
                ('Électricité', '$720.25', 'https://i.pravatar.cc/60?img=12'),
                ('Charbon', '$420.83', 'https://i.pravatar.cc/60?img=48'),
            ]

            for name, price, avatar in data:
                with ui.row().classes('w-full items-center justify-between').style(
                    'padding: 12px 0; border-bottom: 1px solid #ececec;'
                ):
                    with ui.row().classes('items-center').style('gap: 12px;'):
                        ui.image(avatar).classes('pm-avatar')
                        ui.label(name).classes('pm-market-name')
                    ui.label(price).classes('pm-market-price')