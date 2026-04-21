from pathlib import Path
import os
import dj_database_url

# Chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# ══════════════════════════════════════════════════════════════
#  DÉTECTION ENVIRONNEMENT AUTO
# ══════════════════════════════════════════════════════════════
# On considère qu'on est en production si la variable RENDER est présente
IS_PRODUCTION = os.environ.get('RENDER', '').lower() == 'true'

# ══════════════════════════════════════════════════════════════
#  1. SÉCURITÉ & SECRETS
# ══════════════════════════════════════════════════════════════
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-dev-key-change-it')

DEBUG = not IS_PRODUCTION

if IS_PRODUCTION:
    # Récupération dynamique du nom d'hôte Render
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    _hosts = os.environ.get('ALLOWED_HOSTS', 'hillaprince.onrender.com')
    ALLOWED_HOSTS = [h.strip() for h in _hosts.split(',') if h.strip()]
    
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# ══════════════════════════════════════════════════════════════
#  2. BASE DE DONNÉES (CORRIGÉE)
# ══════════════════════════════════════════════════════════════
if IS_PRODUCTION:
    # On récupère l'URL de la base (PostgreSQL Docker ou Render)
    # Assurez-vous que DATABASE_URL est bien définie dans votre dashboard Render
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
    # Option cruciale pour forcer le SSL sur les connexions distantes
    DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}
    
    # Sécurité au cas où dj_database_url échouerait (évite ImproperlyConfigured)
    if not DATABASES['default'].get('ENGINE'):
         raise RuntimeError("DATABASE_URL est vide ou mal configurée sur Render.")
else:
    # Local (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ══════════════════════════════════════════════════════════════
#  3. APPLICATIONS & MIDDLEWARE
# ══════════════════════════════════════════════════════════════
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_ckeditor_5',
    'api', # Votre application
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # 2ème position obligatoire
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'api' / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

WSGI_APPLICATION = 'portfolio.wsgi.application'

# ══════════════════════════════════════════════════════════════
#  4. SÉCURITÉ HTTPS (PROD UNIQUEMENT)
# ══════════════════════════════════════════════════════════════
if IS_PRODUCTION:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000 # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    CSRF_TRUSTED_ORIGINS = ['https://hillaprince.onrender.com']

# ══════════════════════════════════════════════════════════════
#  5. FICHIERS STATIQUES & MEDIA
# ══════════════════════════════════════════════════════════════
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Dossier où React construit ses fichiers (dist/)
REACT_ASSETS_DIR = BASE_DIR / 'react_assets'
# On n'utilise pas .exists() ici pour éviter les erreurs de build initial
STATICFILES_DIRS = [REACT_ASSETS_DIR] 

# Compression et cache WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ══════════════════════════════════════════════════════════════
#  6. REST FRAMEWORK & CORS
# ══════════════════════════════════════════════════════════════
CORS_ALLOWED_ORIGINS = [
    'https://hillaprince.onrender.com',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
] if IS_PRODUCTION else []

CORS_ALLOW_ALL_ORIGINS = not IS_PRODUCTION

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
}

# Internationalisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Ndjamena'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKEDITOR 5
CKEDITOR_5_FILE_STORAGE = 'api.storage.ArticleImageStorage'
CKEDITOR_5_UPLOAD_FILE_TYPES = ['jpeg', 'jpg', 'png', 'gif', 'webp', 'svg']
CKEDITOR_5_MAX_FILE_SIZE = 10
CKEDITOR_5_CONFIGS = {'article': {'height': '600px', 'toolbar': ['heading', '|', 'bold', 'italic', 'link', 'insertImage', 'codeBlock']}}

# ══════════════════════════════════════════════════════════════
#  7. LOGGING
# ══════════════════════════════════════════════════════════════
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'secure': {'format': '[{levelname}] {asctime} {name} — {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'secure'},
    },
    'loggers': {
        'django.utils.autoreload': {'level': 'INFO'}, # Masque les logs de scan de fichiers
        'django.db.backends': {'level': 'WARNING'},
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
}
