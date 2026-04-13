# app/layouts/app_layout.py
# =========================
from typing import Callable
from nicegui import ui


def app_layout(content: Callable[[], None]) -> None:
    ui.add_head_html('''
    <style>
        body {
            background: linear-gradient(180deg, #f3f4f7 0%, #eef1f4 100%);
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }
        .pm-root {
            min-height: 100vh;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .pm-device-frame {
            width: 410px;
            min-height: 860px;
            background: #dfe3e8;
            border-radius: 48px;
            padding: 18px;
            box-shadow: 0 20px 50px rgba(0,0,0,.10);
            position: relative;
        }
        .pm-device-frame::before {
            content: '';
            position: absolute;
            top: 22px;
            left: 50%;
            transform: translateX(-50%);
            width: 150px;
            height: 20px;
            background: #f5f6f8;
            border-radius: 0 0 16px 16px;
            z-index: 2;
        }
        .pm-device-screen {
            width: 100%;
            min-height: 824px;
            background: #ffffff;
            border-radius: 38px;
            overflow: hidden;
            position: relative;
        }
        .pm-safe-zone {
            min-height: 824px;
            padding: 42px 24px 24px 24px;
        }
        .pm-bottom-bar {
            width: 120px;
            height: 6px;
            border-radius: 999px;
            background: #7d7d7d;
            opacity: .7;
            margin: 18px auto 0 auto;
        }
    </style>
    ''')

    with ui.element('div').classes('pm-root'):
        with ui.element('div').classes('pm-device-frame'):
            with ui.element('div').classes('pm-device-screen'):
                with ui.element('div').classes('pm-safe-zone'):
                    content()
            ui.element('div').classes('pm-bottom-bar')