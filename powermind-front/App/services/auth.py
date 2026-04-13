from nicegui import ui
from database import get_connection
import hashlib

def require_login():
    """Décorateur pour protéger les routes."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Vérif session (simplifiée)
            if not hasattr(ui.context.client, 'user_id'):
                ui.notify("Veuillez vous connecter", color='negative')
                ui.navigate.to('/connexion')
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator