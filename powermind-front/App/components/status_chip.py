from nicegui import ui


CHIP_STYLES = {
    'economique': 'background:#b8b4b5;color:#ffffff;',
    'ecologique': 'background:#6fc156;color:#ffffff;',
    'confort': 'background:#2568e8;color:#ffffff;',
    'manuel': 'background:#f26a72;color:#ffffff;',
    'auto': 'background:#7fc45b;color:#ffffff;',
}


def render_status_chip(label: str, variant: str = 'economique') -> None:
    style = CHIP_STYLES.get(variant, CHIP_STYLES['economique'])
    ui.add_head_html('''
    <style>
        .pm-status-chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 10px 16px;
            border-radius: 999px;
            font-size: .98rem;
            font-weight: 700;
            box-shadow: 0 6px 14px rgba(0,0,0,.10);
            min-width: 132px;
        }
    </style>
    ''')
    ui.html(f'<div class="pm-status-chip" style="{style}">{label}</div>')