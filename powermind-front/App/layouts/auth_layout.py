# app/layouts/auth_layout.py
# =========================
from typing import Callable
from nicegui import ui


def auth_layout(content: Callable[[], None]) -> None:
    ui.add_head_html('''
    <style>
        body { background: #f4f5f7; }
        .pm-phone-shell {
            width: 390px;
            min-height: 844px;
            margin: 24px auto;
            background: white;
            border-radius: 42px;
            box-shadow: 0 18px 40px rgba(0,0,0,.08);
            position: relative;
            overflow: hidden;
        }
        .pm-phone-shell::before {
            content: '';
            position: absolute;
            top: 14px;
            left: 50%;
            transform: translateX(-50%);
            width: 145px;
            height: 26px;
            border-radius: 0 0 18px 18px;
            background: #eef0f4;
            z-index: 5;
        }
        .pm-phone-content {
            min-height: 844px;
            padding: 42px 28px 28px 28px;
            display: flex;
            flex-direction: column;
        }
        .pm-title {
            font-size: 2rem;
            font-weight: 700;
            color: #39424e;
            line-height: 1.15;
            margin-bottom: 12px;
        }
        .pm-subtle-line {
            width: 100%;
            height: 2px;
            background: #ededed;
            border-radius: 999px;
            margin: 10px 0 24px 0;
            position: relative;
        }
        .pm-subtle-line::after {
            content: '';
            position: absolute;
            right: 0;
            width: 42%;
            height: 2px;
            background: #424b57;
            border-radius: 999px;
        }
        .pm-back {
            color: #eb6b74;
            font-size: 24px;
            font-weight: 700;
            line-height: 1;
            cursor: pointer;
        }
        .pm-field-label {
            font-size: .92rem;
            font-weight: 600;
            color: #eb6b74;
            margin-top: 16px;
            margin-bottom: 4px;
        }
        .pm-footer-note {
            color: #9ba3ad;
            font-size: .80rem;
            text-align: center;
            margin-top: 20px;
        }
    </style>
    ''')

    with ui.column().classes('w-full items-center'):
        with ui.element('div').classes('pm-phone-shell'):
            with ui.element('div').classes('pm-phone-content'):
                content()

