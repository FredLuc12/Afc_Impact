# app/layouts/dashboard_layout.py
# =========================
from typing import Callable
from nicegui import ui
from app.components.sidebar import render_sidebar
from app.components.topbar import render_topbar


def dashboard_layout(title: str, content: Callable[[], None], show_back: bool = False) -> None:
    ui.add_head_html('''
    <style>
        body { background: #f4f5f7; }
        .pm-app-shell {
            width: 390px;
            min-height: 844px;
            margin: 24px auto;
            background: #ffffff;
            border-radius: 42px;
            overflow: hidden;
            position: relative;
            box-shadow: 0 18px 40px rgba(0,0,0,.08);
        }
        .pm-app-shell::before {
            content: '';
            position: absolute;
            top: 14px;
            left: 50%;
            transform: translateX(-50%);
            width: 145px;
            height: 26px;
            border-radius: 0 0 18px 18px;
            background: #eef0f4;
            z-index: 10;
        }
        .pm-app-content {
            min-height: 844px;
            padding: 42px 26px 26px 26px;
            background: #ffffff;
        }
        .pm-page-title {
            font-size: 2rem;
            font-weight: 700;
            color: #3f4854;
            line-height: 1.2;
            margin-bottom: 12px;
        }
        .pm-section-line {
            width: 100%;
            height: 2px;
            background: #ededed;
            border-radius: 999px;
            margin: 12px 0 24px 0;
            position: relative;
        }
        .pm-section-line::after {
            content: '';
            position: absolute;
            right: 0;
            width: 42%;
            height: 2px;
            background: #424b57;
            border-radius: 999px;
        }
        .pm-kpi-card {
            background: #fafafa;
            border-radius: 18px;
            padding: 16px;
            box-shadow: inset 0 0 0 1px rgba(0,0,0,.03);
        }
        .pm-soft-btn {
            border-radius: 16px;
            padding: 12px 18px;
            font-weight: 700;
            color: white;
            box-shadow: 0 8px 18px rgba(0,0,0,.12);
        }
        .pm-chip {
            padding: 10px 16px;
            border-radius: 999px;
            color: #fff;
            font-weight: 700;
            box-shadow: 0 6px 15px rgba(0,0,0,.10);
        }
        .pm-muted {
            color: #98a1ab;
            font-size: .88rem;
        }
    </style>
    ''')

    drawer = ui.left_drawer(top_corner=True, bottom_corner=True).classes(
        'bg-white shadow-xl rounded-r-3xl'
    )
    render_sidebar(drawer)

    with ui.column().classes('w-full items-center'):
        with ui.element('div').classes('pm-app-shell'):
            with ui.element('div').classes('pm-app-content'):
                render_topbar(title=title, drawer=drawer, show_back=show_back)
                with ui.column().classes('w-full gap-4'):
                    content()

