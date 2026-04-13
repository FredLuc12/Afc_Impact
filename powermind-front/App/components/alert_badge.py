from nicegui import ui


ALERT_STYLES = {
    'info': {
        'bg': '#e8f2ff',
        'text': '#2f87e8',
        'dot': '#2f87e8',
    },
    'success': {
        'bg': '#e8f7ea',
        'text': '#58b85d',
        'dot': '#58b85d',
    },
    'warning': {
        'bg': '#fff3e8',
        'text': '#ef9b47',
        'dot': '#ef9b47',
    },
    'danger': {
        'bg': '#fff0f2',
        'text': '#ea6a73',
        'dot': '#ea6a73',
    },
}


def render_alert_badge(label: str, variant: str = 'info') -> None:
    style = ALERT_STYLES.get(variant, ALERT_STYLES['info'])

    ui.add_head_html('''
    <style>
        .pm-alert-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border-radius: 999px;
            font-size: .88rem;
            font-weight: 700;
            letter-spacing: .01em;
        }
        .pm-alert-dot {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            display: inline-block;
        }
    </style>
    ''')

    ui.html(
        f'<div class="pm-alert-badge" style="background:{style["bg"]};color:{style["text"]};">'
        f'<span class="pm-alert-dot" style="background:{style["dot"]};"></span>'
        f'{label}'
        f'</div>'
    )