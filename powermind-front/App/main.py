# app/main.py
from nicegui import app, ui
from app.config import settings
from app.routes import register_routes

def configure_app() -> None:
    # Note: app.storage.user n'est accessible que LORS d'une requête client.
    # On ne peut pas le remplir ici globalement sans contexte de page.
    pass

def startup() -> None:
    configure_app()
    register_routes()

# SUPPRIMER l'appel direct à startup() ici

if __name__ in {'__main__', '__mp_main__'}:
    # On enregistre les routes ICI, juste avant de lancer le serveur
    startup() 
    
    ui.run(
        host=settings.host,
        port=settings.port,
        title=settings.app_title,
        favicon=settings.favicon,
        reload=settings.reload,
        dark=settings.dark,
        storage_secret=settings.storage_secret,
    )