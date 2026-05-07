"""
settings_prod.py — Production Render
"""
import os
import dj_database_url
from .settings import (
    BASE_DIR, INSTALLED_APPS, AUTH_PASSWORD_VALIDATORS,
    LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ, DEFAULT_AUTO_FIELD,
    REST_FRAMEWORK, CKEDITOR_5_CONFIGS, CKEDITOR_5_FILE_STORAGE,
    CKEDITOR_5_MAX_FILE_SIZE, CKEDITOR_5_UPLOAD_FILE_TYPES,
    ROOT_URLCONF, WSGI_APPLICATION,
)

SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')
DEBUG       = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

INSTALLED_APPS = INSTALLED_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}
    }

# ── Statiques ─────────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ⚠️ PAS CompressedManifest — ça renomme les fichiers et casse index.html
# WhiteNoise sert quand même les fichiers compressés automatiquement
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Les assets React (générés par Vite) sont inclus via STATICFILES_DIRS
REACT_ASSETS_DIR = BASE_DIR / 'react_assets'
STATICFILES_DIRS = [REACT_ASSETS_DIR] if REACT_ASSETS_DIR.exists() else []

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

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

CORS_ALLOWED_ORIGINS   = []
CORS_ALLOW_ALL_ORIGINS = False

if not DEBUG:
    SECURE_PROXY_SSL_HEADER        = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT            = True
    SESSION_COOKIE_SECURE          = True
    CSRF_COOKIE_SECURE             = True
    CSRF_TRUSTED_ORIGINS           = [
        f"https://{h}" for h in ALLOWED_HOSTS
        if h not in ('localhost', '127.0.0.1')
    ]
    SECURE_HSTS_SECONDS            = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'INFO'},
}

CSRF_TRUSTED_ORIGINS = [
    "https://hillaprince.com",
    "https://www.hillaprince.com",
]
