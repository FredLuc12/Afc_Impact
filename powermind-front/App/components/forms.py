from nicegui import ui


def render_input_field(label: str, placeholder: str = '', password: bool = False):
    ui.add_head_html('''
    <style>
        .pm-form-group { width: 100%; margin-bottom: 20px; }
        .pm-form-label {
            display: block;
            margin-bottom: 8px;
            color: #ea6a73;
            font-size: .92rem;
            font-weight: 600;
        }
        .pm-form-input {
            width: 100%;
            border: none;
            border-bottom: 1.5px solid #e6e6e6;
            background: transparent;
            padding: 10px 2px 8px 2px;
            color: #3f4854;
            font-size: 1rem;
            outline: none;
        }
        .pm-form-input::placeholder {
            color: #c8cdd3;
        }
        .pm-form-input:focus {
            border-bottom-color: #ea6a73;
        }
    </style>
    ''')

    with ui.element('div').classes('pm-form-group'):
        ui.label(label).classes('pm-form-label')
        return ui.input(placeholder=placeholder, password=password).classes('pm-form-input')