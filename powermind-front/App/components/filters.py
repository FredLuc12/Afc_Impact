from nicegui import ui


def render_segmented_filter(options: list[str], active: str | None = None, on_change=None) -> None:
    selected = active or (options[0] if options else '')

    ui.add_head_html('''
    <style>
        .pm-filter-wrap {
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 22px;
            margin: 8px 0 18px 0;
        }
        .pm-filter-item {
            position: relative;
            color: #b2b8bf;
            font-size: .95rem;
            cursor: pointer;
            padding-bottom: 8px;
        }
        .pm-filter-item.active {
            color: #3f4854;
            font-weight: 600;
        }
        .pm-filter-item.active::after {
            content: '';
            position: absolute;
            left: 0;
            right: 0;
            bottom: 0;
            height: 2px;
            border-radius: 999px;
            background: #434c57;
        }
    </style>
    ''')

    with ui.element('div').classes('pm-filter-wrap'):
        for option in options:
            cls = 'pm-filter-item active' if option == selected else 'pm-filter-item'
            el = ui.label(option).classes(cls)
            if on_change:
                el.on('click', lambda e, value=option: on_change(value))