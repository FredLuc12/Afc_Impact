# app/main.py

from nicegui import app, ui

from app.config import settings
from app.routes import register_routes


def configure_app() -> None:
    app.storage.user['app_name'] = settings.app_name
    app.storage.user['app_version'] = settings.app_version

    ui.colors(
        primary='#0f766e',
        secondary='#1f2937',
        accent='#14b8a6',
        positive='#22c55e',
        negative='#ef4444',
        warning='#f59e0b',
        info='#3b82f6',
    )

    ui.add_head_html('''
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="PowerMind - suivi énergétique intelligent">
    ''')


def startup() -> None:
    configure_app()
    register_routes()


startup()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        host=settings.host,
        port=settings.port,
        title=settings.app_title,
        favicon=settings.favicon,
        reload=settings.reload,
        dark=settings.dark,
        storage_secret=settings.storage_secret,
    )