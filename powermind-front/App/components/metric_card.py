from nicegui import ui


def render_metric_card(title: str, value: str, subtitle: str = '', accent: str = '#6e77f6') -> None:
    ui.add_head_html('''
    <style>
        .pm-metric-card {
            background: #fbfbfb;
            border-radius: 18px;
            padding: 16px;
            box-shadow: inset 0 0 0 1px rgba(0,0,0,.03);
            min-height: 120px;
        }
        .pm-metric-title {
            color: #a1a8b0;
            font-size: .92rem;
            margin-bottom: 8px;
        }
        .pm-metric-value {
            color: #39424e;
            font-size: 2rem;
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 6px;
        }
        .pm-metric-subtitle {
            color: #9da5af;
            font-size: .88rem;
        }
        .pm-metric-dot {
            width: 10px;
            height: 10px;
            border-radius: 999px;
            display: inline-block;
            margin-right: 8px;
        }
    </style>
    ''')

    with ui.element('div').classes('pm-metric-card'):
        ui.label(title).classes('pm-metric-title')
        ui.label(value).classes('pm-metric-value')
        if subtitle:
            ui.html(
                f'<div class="pm-metric-subtitle"><span class="pm-metric-dot" style="background:{accent};"></span>{subtitle}</div>'
            )