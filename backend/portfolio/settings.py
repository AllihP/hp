from pathlib import Path
import os
import dj_database_url

# Chemin de base
BASE_DIR = Path(__file__).resolve().parent.parent

# ══════════════════════════════════════════════════════════════
#  DÉTECTION DE L'ENVIRONNEMENT
# ══════════════════════════════════════════════════════════════
# On active la prod si RENDER=true ou si une DATABASE_URL est présente
IS_PRODUCTION = os.environ.get('RENDER', '').lower() == 'true' or 'DATABASE_URL' in os.environ

# ══════════════════════════════════════════════════════════════
#  1. SÉCURITÉ & SECRETS
# ══════════════════════════════════════════════════════════════
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-dev-key-valide-uniquement-en-local')

DEBUG = not IS_PRODUCTION

if IS_PRODUCTION:
    # Récupération dynamique du nom d'hôte de Render
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    _hosts = os.environ.get('ALLOWED_HOSTS', 'hillaprince.onrender.com')
    ALLOWED_HOSTS = [h.strip() for h in _hosts.split(',') if h.strip()]
    
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# ══════════════════════════════════════════════════════════════
#  2. BASE DE DONNÉES (CORRIGÉE POUR RENDER & EXTERNE)
# ══════════════════════════════════════════════════════════════
DATABASE_URL = os.environ.get('DATABASE_URL')

if IS_PRODUCTION and DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
    # Important pour Neon, Supabase, etc.
    DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}
else:
    # Mode Local (SQLite) pour ne pas bloquer le collectstatic ou le dev
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    
# Autoriser l'envoi de cookies/sessions via CORS
    CORS_ALLOW_CREDENTIALS = True
    
    # Indispensable pour que Django accepte le jeton CSRF venant du frontend
    CSRF_TRUSTED_ORIGINS = [
        'https://hillaprince.onrender.com',
    ]



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
    # Packages tiers
    'rest_framework',
    'corsheaders',
    'django_ckeditor_5',
    # Votre application
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Doit être juste après SecurityMiddleware
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
#  4. SÉCURITÉ HTTPS (PRODUCTION)
# ══════════════════════════════════════════════════════════════
if IS_PRODUCTION:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    CSRF_TRUSTED_ORIGINS = ['https://hillaprince.onrender.com']
    # Empêche de charger ton site dans un <iframe> (évite le Clickjacking)
    X_FRAME_OPTIONS = 'DENY'
    
    # Force le navigateur à ne pas deviner le type de contenu (évite le XSS)
    SECURE_CONTENT_TYPE_NOSNIFF = True
    
    # Politique de referer : ne pas envoyer ton URL à des sites externes
    SECURE_REFERRER_POLICY = 'same-origin'
    
    # Content Security Policy (CSP) - Optionnel mais puissant
    # Autorise uniquement les scripts venant de ton domaine
    CSP_DEFAULT_SRC = ("'self'",)
    CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")

# ══════════════════════════════════════════════════════════════
#  5. FICHIERS STATIQUES & REACT
# ══════════════════════════════════════════════════════════════
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Dossier où arrive le build de React
REACT_ASSETS_DIR = BASE_DIR / 'react_assets'
STATICFILES_DIRS = [REACT_ASSETS_DIR]

# WhiteNoise pour servir les fichiers statiques de manière efficace
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ══════════════════════════════════════════════════════════════
#  6. CORS & API
# ══════════════════════════════════════════════════════════════
if IS_PRODUCTION:
    CORS_ALLOWED_ORIGINS = ['https://hillaprince.onrender.com']
else:
    CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
}

# Configuration par défaut
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Ndjamena'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKEDITOR 5
CKEDITOR_5_FILE_STORAGE = 'api.storage.ArticleImageStorage'
CKEDITOR_5_CONFIGS = {
    'article': {
        'height': '400px',
        'toolbar': ['heading', '|', 'bold', 'italic', 'link', 'insertImage', 'codeBlock'],
    }
}

# ══════════════════════════════════════════════════════════════
#  7. LOGGING
# ══════════════════════════════════════════════════════════════
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '[{levelname}] {asctime} {name} — {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
}
