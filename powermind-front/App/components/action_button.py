from nicegui import ui


BUTTON_STYLES = {
    'green': 'background:#78be4d;color:white;',
    'coral': 'background:#f45f6c;color:white;',
    'blue': 'background:#2d87e8;color:white;',
    'light': 'background:#f7f7f8;color:#3f4854;border:1px solid #ececec;',
}


def render_action_button(label: str, on_click=None, color: str = 'green', full: bool = True) -> None:
    style = BUTTON_STYLES.get(color, BUTTON_STYLES['green'])
    width = 'width:100%;' if full else 'width:auto;'

    ui.add_head_html('''
    <style>
        .pm-action-btn {
            border: none;
            border-radius: 10px;
            min-height: 52px;
            padding: 0 18px;
            font-size: 1rem;
            font-weight: 700;
            box-shadow: 0 8px 18px rgba(0,0,0,.10);
            cursor: pointer;
            transition: transform .16s ease, opacity .16s ease;
        }
        .pm-action-btn:hover {
            transform: translateY(-1px);
            opacity: .96;
        }
    </style>
    ''')

    button = ui.html(f'<button class="pm-action-btn" style="{style}{width}">{label}</button>')
    if on_click:
        button.on('click', on_click)