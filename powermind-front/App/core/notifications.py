# app/core/notifications.py

from nicegui import ui


def notify_success(message: str) -> None:
    ui.notify(message, color='positive')


def notify_error(message: str) -> None:
    ui.notify(message, color='negative')


def notify_warning(message: str) -> None:
    ui.notify(message, color='warning')


def notify_info(message: str) -> None:
    ui.notify(message, color='info')