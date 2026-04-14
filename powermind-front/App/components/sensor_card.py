from nicegui import ui


_STATUS_META = {
    'online': {'label': 'En ligne', 'dot': '#7dc86e', 'bg': '#edf8ec'},
    'warning': {'label': 'À surveiller', 'dot': '#f5a623', 'bg': '#fff5e8'},
    'offline': {'label': 'Hors ligne', 'dot': '#ef6b73', 'bg': '#fdecee'},
    'idle': {'label': 'Veille', 'dot': '#9ca4ae', 'bg': '#f1f3f5'},
}

_COLOR_META = {
    'green': {'soft': '#edf8ec', 'accent': '#7dc86e', 'icon': '#4cae50'},
    'blue': {'soft': '#edf4ff', 'accent': '#76a8ff', 'icon': '#4f7df3'},
    'cyan': {'soft': '#ebfbfb', 'accent': '#74d7d3', 'icon': '#33b8b0'},
    'orange': {'soft': '#fff4e8', 'accent': '#f8bf7a', 'icon': '#ee9a32'},
    'purple': {'soft': '#f2eefe', 'accent': '#b7a3ff', 'icon': '#7b61ff'},
    'red': {'soft': '#fdecee', 'accent': '#f4a0aa', 'icon': '#ef6b73'},
    'gray': {'soft': '#f4f6f8', 'accent': '#c8ced6', 'icon': '#7f8a96'},
}



def render_sensor_card(
    title: str,
    value: str,
    unit: str = '',
    status: str = 'online',
    icon: str = 'sensors',
    color: str = 'green',
) -> None:
    status_meta = _STATUS_META.get(status, _STATUS_META['online'])
    color_meta = _COLOR_META.get(color, _COLOR_META['gray'])

    ui.add_head_html('''
    <style>
        .pm-sensor-card {
            background: #ffffff;
            border-radius: 18px;
            border: 1px solid #eef1f4;
            box-shadow: 0 10px 24px rgba(31, 41, 55, 0.06);
            padding: 14px;
            min-width: 160px;
            flex: 1 1 160px;
        }
        .pm-sensor-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 14px;
        }
        .pm-sensor-icon-box {
            width: 42px;
            height: 42px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        .pm-sensor-title {
            color: #55606d;
            font-size: 13px;
            font-weight: 600;
            line-height: 1.3;
        }
        .pm-sensor-status {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            border-radius: 999px;
            padding: 4px 8px;
            font-size: 11px;
            font-weight: 700;
            white-space: nowrap;
        }
        .pm-sensor-dot {
            width: 7px;
            height: 7px;
            border-radius: 999px;
            display: inline-block;
        }
        .pm-sensor-value {
            color: #3f4854;
            font-size: 24px;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 6px;
        }
        .pm-sensor-unit {
            color: #97a0aa;
            font-size: 12px;
            font-weight: 600;
        }
    </style>
    ''')

    with ui.card().classes('pm-sensor-card'):
        with ui.row().classes('pm-sensor-top w-full no-wrap'):
            with ui.row().classes('items-start no-wrap').style('gap: 10px; flex: 1;'):
                with ui.element('div').classes('pm-sensor-icon-box').style(
                    f'background:{color_meta["soft"]};'
                ):
                    ui.icon(icon).style(f'color:{color_meta["icon"]}; font-size: 22px;')
                ui.label(title).classes('pm-sensor-title')

            with ui.element('div').classes('pm-sensor-status').style(
                f'background:{status_meta["bg"]}; color:{status_meta["dot"]};'
            ):
                ui.element('span').classes('pm-sensor-dot').style(f'background:{status_meta["dot"]};')
                ui.label(status_meta['label']).style('font-size:11px; font-weight:700;')

        ui.label(value).classes('pm-sensor-value')
        if unit:
            ui.label(unit).classes('pm-sensor-unit')