from nicegui import ui


def render_stat_card(title: str, lines: list[tuple[str, str]]) -> None:
    ui.add_head_html('''
    <style>
        .pm-stat-card {
            width: 100%;
            background: white;
            border-radius: 16px;
            padding: 10px 0;
        }
        .pm-stat-title {
            text-align: right;
            color: #434c57;
            font-weight: 700;
            padding: 0 4px 8px 4px;
        }
        .pm-stat-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 4px;
            border-top: 1px solid #f0f0f0;
        }
        .pm-stat-left {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #666f79;
        }
        .pm-stat-avatar {
            width: 28px;
            height: 28px;
            border-radius: 999px;
            background: linear-gradient(135deg, #e8e8e8, #cfcfcf);
        }
        .pm-stat-value {
            color: #8d95a0;
            font-size: .95rem;
        }
    </style>
    ''')

    with ui.element('div').classes('pm-stat-card'):
        ui.label(title).classes('pm-stat-title')
        for label, value in lines:
            with ui.element('div').classes('pm-stat-row'):
                with ui.element('div').classes('pm-stat-left'):
                    ui.element('div').classes('pm-stat-avatar')
                    ui.label(label)
                ui.label(value).classes('pm-stat-value')