# app/core/security.py

from __future__ import annotations
from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import app, ui
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.session import SessionManager
from app.constants import (
    ROUTE_ADMIN,
    ROUTE_DASHBOARD,
    ROUTE_LOGIN,
    ROUTE_REGISTER
)

# On définit les routes qui ne nécessitent JAMAIS de connexion
PUBLIC_ROUTES = {ROUTE_LOGIN, ROUTE_REGISTER, '/forgot-password', '/forbidden', '/404'}
ADMIN_ROLES = {'admin', 'super_admin'}
TECH_ROLES = {'admin', 'super_admin', 'technicien'}
USER_ROLES = {'user', 'admin', 'super_admin', 'technicien'}

def is_public_path(path: str) -> bool:
    """Détermine si un chemin est accessible sans authentification."""
    # Nettoyage du path (on enlève les paramètres après ?)
    clean_path = path.split('?')[0]
    
    # 1. Routes de base
    if clean_path in PUBLIC_ROUTES:
        return True
    
    # 2. Ressources internes NiceGUI, FastAPI et Statiques
    # On autorise tout ce qui commence par ces préfixes pour éviter les boucles
    internal_prefixes = [
        '/_nicegui', 
        '/static', 
        '/favicon', 
        '/_pywebview', 
        '/asset',
        '/_starlette'
    ]
    
    if any(clean_path.startswith(p) for p in internal_prefixes):
        return True
        
    return False

def require_auth() -> bool:
    if not SessionManager.is_authenticated():
        ui.navigate.to(ROUTE_LOGIN)
        return False
    return True

def require_role(*roles: str) -> bool:
    if not require_auth():
        return False
    current_role = SessionManager.get_role()
    if current_role not in roles:
        ui.notify("Accès refusé", color='negative')
        ui.navigate.to(ROUTE_LOGIN)
        return False
    return True

def require_same_installation(installation_id: str | None) -> bool:
    if not require_auth(): return False
    if SessionManager.get_role() in ADMIN_ROLES: return True
    current_id = SessionManager.get_installation_id()
    if not current_id or str(current_id) != str(installation_id):
        ui.navigate.to(ROUTE_LOGIN)
        return False
    return True

def get_default_redirect_path() -> str:
    role = SessionManager.get_role()
    installation_id = SessionManager.get_installation_id()
    if role in ADMIN_ROLES:
        return ROUTE_ADMIN
    if installation_id:
        return f'{ROUTE_DASHBOARD}/{installation_id}'
    return ROUTE_LOGIN

@app.add_middleware
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # DEBUG : Décommente la ligne suivante pour voir les chemins bloqués dans ton terminal
        print(f"Middleware inspecte : {path} | Public: {is_public_path(path)} | Auth: {SessionManager.is_authenticated()}")

        # RÈGLE 1 : Si c'est un chemin public ou interne, on laisse passer sans condition
        if is_public_path(path):
            return await call_next(request)

        # RÈGLE 2 : Si l'utilisateur n'est pas connecté
        if not SessionManager.is_authenticated():
            # Si on essaie d'aller à la racine ou ailleurs, on force vers LOGIN
            if path != ROUTE_LOGIN:
                return RedirectResponse(f'{ROUTE_LOGIN}?redirect_to={path}')

        # RÈGLE 3 : Si on arrive ici, soit on est connecté, soit on est sur le login
        return await call_next(request)