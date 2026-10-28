"""
settings_prod.py — Production Render (Docker)

Hérite de TOUS les réglages de settings.py (sessions courtes, validation
des mots de passe, limitation de débit, logs de sécurité, CKEditor…),
puis force les valeurs propres à la production.
"""
import os
import dj_database_url
from .settings import *  # noqa: F401,F403
from .settings import BASE_DIR

import sys
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ── Clé secrète : obligatoire hors DEBUG ──────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', '')
_WEAK_KEYS = ('', 'change-me-in-production')
_is_building = any(arg in sys.argv for arg in ('collectstatic', 'check'))
if not DEBUG and not _is_building and (SECRET_KEY in _WEAK_KEYS or 'insecure' in SECRET_KEY
                  or len(SECRET_KEY) < 40):
    raise RuntimeError(
        "FATAL: SECRET_KEY absente ou trop faible (40 caractères minimum).\n"
        "Définissez SECRET_KEY dans Render → Environment."
    )
if not SECRET_KEY:
    SECRET_KEY = 'temporary-build-key-strictly-for-collectstatic-40chars'

# ── Hosts ─────────────────────────────────────────────────────
_hosts = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in _hosts.split(',') if h.strip()]
_render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')
if _render_host and _render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_render_host)
for _d in ('hillaprince.com', 'www.hillaprince.com'):
    if _d not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_d)

_LOCAL = ('localhost', '127.0.0.1', '0.0.0.0')

# ── Base de données ───────────────────────────────────────────
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG,   # SSL obligatoire en prod
        )
    }
else:
    DATABASES = {
        'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}
    }

# ── Cache partagé (limitation de débit) ───────────────────────
# Nécessite : python manage.py createcachetable
CACHES = {'default': {
    'BACKEND':  'django.core.cache.backends.db.DatabaseCache',
    'LOCATION': 'django_cache',
}}

# ── CORS ──────────────────────────────────────────────────────
_cors_env = os.environ.get('CORS_ALLOWED_ORIGINS', '')
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = False
_cors_list = [
    o.strip() if o.strip().startswith(('http://', 'https://')) else f"https://{o.strip()}"
    for o in _cors_env.split(',') if o.strip()
]
CORS_ALLOWED_ORIGINS   = list(set(_cors_list) | {
    f"https://{h}" for h in ALLOWED_HOSTS if h not in _LOCAL
} | {
    'https://hillaprince.com', 'https://www.hillaprince.com'
})

# ── HTTPS & en-têtes (hors DEBUG) ─────────────────────────────
if not DEBUG:
    SECURE_PROXY_SSL_HEADER        = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT            = True
    SESSION_COOKIE_SECURE          = True
    CSRF_COOKIE_SECURE             = True
    CSRF_TRUSTED_ORIGINS           = list({
        f"https://{h}" for h in ALLOWED_HOSTS if h not in _LOCAL
    } | set(CORS_ALLOWED_ORIGINS))
    SECURE_HSTS_SECONDS            = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD            = True
    SECURE_CONTENT_TYPE_NOSNIFF    = True
    SECURE_REFERRER_POLICY         = 'strict-origin-when-cross-origin'
    X_FRAME_OPTIONS                = 'DENY'
else:
    SECURE_SSL_REDIRECT   = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE    = False
    SECURE_HSTS_SECONDS   = 0
