from nicegui import ui


def confirm_dialog(title: str, message: str, on_confirm=None, confirm_label: str = 'OK', cancel_label: str = 'CANCEL'):
    ui.add_head_html('''
    <style>
        .pm-dialog-card {
            width: 300px;
            border-radius: 14px;
            background: #ffffff;
            box-shadow: 0 16px 32px rgba(0,0,0,.16);
            overflow: hidden;
        }
        .pm-dialog-header {
            background: #5daef0;
            min-height: 70px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
            font-weight: 300;
        }
        .pm-dialog-body {
            padding: 16px 16px 10px 16px;
            color: #4a5360;
            font-size: .95rem;
        }
        .pm-dialog-actions {
            display: flex;
            justify-content: flex-end;
            gap: 8px;
            padding: 0 12px 12px 12px;
        }
        .pm-dialog-btn {
            border: none;
            background: transparent;
            color: #606975;
            font-size: .85rem;
            padding: 8px 12px;
            border-radius: 8px;
            cursor: pointer;
        }
        .pm-dialog-btn.primary {
            background: #2f95f3;
            color: white;
        }
    </style>
    ''')

    dialog = ui.dialog()
    with dialog, ui.card().classes('pm-dialog-card'):
        ui.label(title).classes('pm-dialog-header')
        ui.label(message).classes('pm-dialog-body')
        with ui.row().classes('pm-dialog-actions'):
            cancel = ui.html(f'<button class="pm-dialog-btn">{cancel_label}</button>')
            confirm = ui.html(f'<button class="pm-dialog-btn primary">{confirm_label}</button>')
            cancel.on('click', dialog.close)
            if on_confirm:
                confirm.on('click', lambda: (on_confirm(), dialog.close()))
            else:
                confirm.on('click', dialog.close)
    return dialog