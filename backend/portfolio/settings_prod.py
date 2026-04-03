"""
settings_prod.py — Production Render
Fix : fichiers statiques admin via WhiteNoise
"""
import os
import dj_database_url
from .settings import BASE_DIR, INSTALLED_APPS, MIDDLEWARE as BASE_MIDDLEWARE

# ── Sécurité ──────────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me')
DEBUG       = os.environ.get('DEBUG', 'False') == 'True'

_hosts = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [h.strip() for h in _hosts.split(',') if h.strip()]

# ── Applications ──────────────────────────────────────────────
INSTALLED_APPS = INSTALLED_APPS

# ── Middleware — WhiteNoise DOIT être en 2ème position ────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # ← juste après Security
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ── Base de données ───────────────────────────────────────────
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
        )
    }
else:
    # Fallback SQLite (dev local)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ── Fichiers statiques — WhiteNoise ──────────────────────────
STATIC_URL   = '/static/'
STATIC_ROOT  = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = []   # vide en prod — tout vient de collectstatic

# ── Médias ────────────────────────────────────────────────────
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ── Templates ─────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'api' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ── CORS ──────────────────────────────────────────────────────
_cors = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:5173,http://localhost:3000'
)
CORS_ALLOWED_ORIGINS   = [o.strip() for o in _cors.split(',') if o.strip()]
CORS_ALLOW_ALL_ORIGINS = False

# ── Autres settings hérités de settings.py ───────────────────
from .settings import (  # noqa
    ROOT_URLCONF, WSGI_APPLICATION, AUTH_PASSWORD_VALIDATORS,
    LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ,
    DEFAULT_AUTO_FIELD, REST_FRAMEWORK,
    CKEDITOR_5_CONFIGS, CKEDITOR_5_FILE_STORAGE,
    CKEDITOR_5_MAX_FILE_SIZE, CKEDITOR_5_UPLOAD_FILE_TYPES,
)

# ── HTTPS (seulement si DEBUG=False) ─────────────────────────
if not DEBUG:
    SECURE_PROXY_SSL_HEADER        = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT            = True
    SESSION_COOKIE_SECURE          = True
    CSRF_COOKIE_SECURE             = True
    SECURE_HSTS_SECONDS            = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF    = True

# ── Logging ───────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'WARNING'},
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'WARNING'),
            'propagate': False,
        },
    },
}
