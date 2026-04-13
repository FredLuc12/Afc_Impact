from nicegui import ui


def render_donut_pair(left_label: str = 'GAZ', left_value: int = 64, right_label: str = 'Electricité', right_value: int = 90) -> None:
    ui.add_head_html('''
    <style>
        .pm-donut-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
            width: 100%;
            margin-top: 8px;
        }
        .pm-donut-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }
        .pm-donut-label {
            color: #b0b7bf;
            font-size: .9rem;
        }
        .pm-ring {
            width: 84px;
            height: 84px;
            border-radius: 50%;
            display: grid;
            place-items: center;
            font-size: 1.55rem;
            font-weight: 700;
            position: relative;
        }
        .pm-ring::after {
            content: '';
            width: 64px;
            height: 64px;
            background: white;
            border-radius: 50%;
            position: absolute;
        }
        .pm-ring-value {
            position: relative;
            z-index: 1;
            font-size: 1.2rem;
            font-weight: 700;
        }
        .pm-mini-chart {
            margin-top: 18px;
            width: 100%;
            background: #fafafa;
            border-radius: 18px;
            padding: 16px 12px 10px 12px;
        }
        .pm-bar-row {
            display: flex;
            align-items: end;
            gap: 8px;
            height: 80px;
        }
        .pm-bar {
            width: 10px;
            border-radius: 2px 2px 0 0;
            background: #919191;
        }
        .pm-bar.red { background: #ef6670; }
        .pm-bar.light-red { background: #f9a0a5; }
        .pm-chart-title {
            margin-top: 10px;
            text-align: right;
            color: #434c57;
            font-weight: 700;
        }
    </style>
    ''')

    left_bg = f'conic-gradient(#86ddb4 {left_value}%, #ececec 0)'
    right_bg = f'conic-gradient(#5c67ec {right_value}%, #ececec 0)'

    with ui.element('div').classes('pm-donut-grid'):
        with ui.element('div').classes('pm-donut-box'):
            ui.label(left_label).classes('pm-donut-label')
            ui.html(f'<div class="pm-ring" style="background:{left_bg};"><span class="pm-ring-value" style="color:#70cfa4;">{left_value}%</span></div>')
        with ui.element('div').classes('pm-donut-box'):
            ui.label(right_label).classes('pm-donut-label')
            ui.html(f'<div class="pm-ring" style="background:{right_bg};"><span class="pm-ring-value" style="color:#5c67ec;">{right_value}%</span></div>')


def render_mini_bar_chart() -> None:
    bars = [48, 56, 64, 40, 72, 58, 64, 65, 34, 56, 48, 78, 55, 72, 40, 57]
    colors = ['pm-bar', 'pm-bar', 'pm-bar', 'pm-bar', 'pm-bar', 'pm-bar', 'pm-bar', 'pm-bar',
              'pm-bar light-red', 'pm-bar red', 'pm-bar light-red', 'pm-bar red',
              'pm-bar light-red', 'pm-bar red', 'pm-bar light-red', 'pm-bar red']

    with ui.element('div').classes('pm-mini-chart'):
        with ui.element('div').classes('pm-bar-row'):
            for h, c in zip(bars, colors):
                ui.html(f'<div class="{c}" style="height:{h}px"></div>')
        ui.label('Tarifs du marché').classes('pm-chart-title')