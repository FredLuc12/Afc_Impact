# app/constants.py

APP_NAME = 'POWERMIND'
APP_SLUG = 'powermind'
APP_VERSION = '0.1.0'
APP_DESCRIPTION = 'Application web de suivi énergétique intelligent'

DEFAULT_TITLE = 'POWERMIND'
DEFAULT_TIMEZONE = 'Europe/Paris'
DEFAULT_DATE_FORMAT = '%d/%m/%Y'
DEFAULT_DATETIME_FORMAT = '%d/%m/%Y %H:%M'
DEFAULT_LANGUAGE = 'fr'

ROLE_ADMIN = 'admin'
ROLE_TECHNICIEN = 'technicien'
ROLE_USER = 'user'
ROLE_SUPER_ADMIN = 'super_admin'

ROLES = [
    ROLE_ADMIN,
    ROLE_TECHNICIEN,
    ROLE_USER,
    ROLE_SUPER_ADMIN,
]

STATUS_OK = 'ok'
STATUS_WARNING = 'warning'
STATUS_ERROR = 'error'
STATUS_OFFLINE = 'offline'

ALERT_CRITICAL = 'critique'
ALERT_HIGH = 'haute'
ALERT_MEDIUM = 'moyenne'
ALERT_LOW = 'faible'

ROUTE_ROOT = '/'
ROUTE_LOGIN = '/login'
ROUTE_REGISTER = '/register'
ROUTE_LOGOUT = '/logout'
ROUTE_HOME = '/home'
ROUTE_DATE_HEURE = '/date-heure'
ROUTE_VALEURS_BASES = '/valeurs-bases'
ROUTE_DASHBOARD = '/dashboard'
ROUTE_ADMIN = '/admin/users'
ROUTE_CONSOMMATION = '/consommation'
ROUTE_INSTALLATIONS = '/installations'
ROUTE_CAPTEURS = '/capteurs'
ROUTE_FORBIDEN = '/forbiden'
ROUTE_FORGOT_PASSWORD = '/forgot-password'
ROUTE_MESURES = '/mesures'
ROUTE_ALERTES = '/alertes'
ROUTE_PROFIL = '/profil'
ROUTE_REGLAGES = '/reglages'
ROUTE_MAINTENANCE = '/maintenance'
ROUTE_404 = '/404'
ROUTE_WAITING = '/waiting'

PUBLIC_ROUTES = {
    ROUTE_ROOT,
    ROUTE_LOGIN,
    ROUTE_REGISTER,
    ROUTE_404,
}

NAV_ITEMS = [
    {'label': 'Accueil', 'icon': 'home', 'path': ROUTE_HOME, 'roles': ROLES},
    {'label': 'Dashboard', 'icon': 'dashboard', 'path': ROUTE_DASHBOARD, 'roles': ROLES},
    {'label': 'Installations', 'icon': 'apartment', 'path': ROUTE_INSTALLATIONS, 'roles': ROLES},
    {'label': 'Capteurs', 'icon': 'sensors', 'path': ROUTE_CAPTEURS, 'roles': ROLES},
    {'label': 'Mesures', 'icon': 'query_stats', 'path': ROUTE_MESURES, 'roles': ROLES},
    {'label': 'Alertes', 'icon': 'warning', 'path': ROUTE_ALERTES, 'roles': ROLES},
    {'label': 'Profil', 'icon': 'person', 'path': ROUTE_PROFIL, 'roles': ROLES},
    {'label': 'Réglages', 'icon': 'settings', 'path': ROUTE_REGLAGES, 'roles': [ROLE_ADMIN, ROLE_TECHNICIEN]},
    {'label': 'Maintenance', 'icon': 'build', 'path': ROUTE_MAINTENANCE, 'roles': [ROLE_ADMIN, ROLE_TECHNICIEN]},
]

DEFAULT_REDIRECT_IF_AUTHENTICATED = ROUTE_DASHBOARD
DEFAULT_REDIRECT_IF_NOT_AUTHENTICATED = ROUTE_LOGIN

TABLE_PROFILES = 'profiles'
TABLE_INSTALLATIONS = 'installations'
TABLE_CAPTEURS = 'capteurs'
TABLE_TYPES_MESURES = 'types_mesure'
TABLE_MESURES = 'mesures'
TABLE_ALERTES = 'alertes'
TABLE_CHOIX_AUTO = 'choix_auto'
