from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ══════════════════════════════════════════════════════════════
#  DÉTECTION ENVIRONNEMENT AUTO
#  IS_PRODUCTION = True sur Render (DATABASE_URL présent)
# ══════════════════════════════════════════════════════════════
DATABASE_URL  = os.environ.get('DATABASE_URL', '')
IS_PRODUCTION = bool(DATABASE_URL) or os.environ.get("RENDER", "") == "true"

# ══════════════════════════════════════════════════════════════
#  1. VARIABLES D'ENVIRONNEMENT & SECRETS
# ══════════════════════════════════════════════════════════════

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-dev-CHANGE-IN-PROD')

# Erreur fatale si clé insécurisée en production
if IS_PRODUCTION and 'insecure' in SECRET_KEY:
    raise RuntimeError(
        "FATAL: SECRET_KEY non sécurisée en production.\n"
        "Définissez SECRET_KEY dans les variables Render → Environment."
    )

# ══════════════════════════════════════════════════════════════
#  2. SÉCURITÉ DE BASE DJANGO
# ══════════════════════════════════════════════════════════════

# DEBUG jamais True en production
DEBUG = not IS_PRODUCTION

# ALLOWED_HOSTS — jamais ['*'] en production
if IS_PRODUCTION:
    _hosts = os.environ.get('ALLOWED_HOSTS', 'hillaprince.onrender.com')
    ALLOWED_HOSTS = [h.strip() for h in _hosts.split(',') if h.strip()]
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

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
    'api',
]

# Middleware — ordre critique pour la sécurité
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',     # 1er — HTTPS redirect
    'whitenoise.middleware.WhiteNoiseMiddleware',         # 2ème — statiques
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',              # avant CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',          # protection CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # anti-clickjacking
]

ROOT_URLCONF     = 'portfolio.urls'
WSGI_APPLICATION = 'portfolio.wsgi.application'

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

# ══════════════════════════════════════════════════════════════
#  BASE DE DONNÉES
# ══════════════════════════════════════════════════════════════
if IS_PRODUCTION:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,    # SSL obligatoire avec PostgreSQL Render
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME':   BASE_DIR / 'db.sqlite3',
        }
    }

# ══════════════════════════════════════════════════════════════
#  MOTS DE PASSE — validation forte
# ══════════════════════════════════════════════════════════════
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ══════════════════════════════════════════════════════════════
#  AUTHENTIFICATION & ACCÈS ADMIN
# ══════════════════════════════════════════════════════════════

# Sessions — expiration courte
SESSION_COOKIE_HTTPONLY             = True   # inaccessible au JS
SESSION_COOKIE_SAMESITE             = 'Lax'
SESSION_COOKIE_AGE                  = 3600   # 1h d'inactivité
SESSION_EXPIRE_AT_BROWSER_CLOSE     = True   # expire à la fermeture
SESSION_SAVE_EVERY_REQUEST          = False

# CSRF
CSRF_COOKIE_HTTPONLY = False  # doit être lisible par JS pour les SPA
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS    = False

# ══════════════════════════════════════════════════════════════
#  HTTPS & CERTIFICATS (production uniquement)
# ══════════════════════════════════════════════════════════════
if IS_PRODUCTION:
    # Redirection HTTP → HTTPS automatique
    SECURE_SSL_REDIRECT                = True
    SECURE_PROXY_SSL_HEADER            = ('HTTP_X_FORWARDED_PROTO', 'https')

    # HSTS — force HTTPS pour 1 an
    SECURE_HSTS_SECONDS                = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS     = True
    SECURE_HSTS_PRELOAD                = True

    # Cookies sécurisés HTTPS uniquement
    SESSION_COOKIE_SECURE              = True
    CSRF_COOKIE_SECURE                 = True

    # Headers de sécurité
    SECURE_CONTENT_TYPE_NOSNIFF        = True  # anti MIME-sniffing
    SECURE_REFERRER_POLICY             = 'strict-origin-when-cross-origin'
    X_FRAME_OPTIONS                    = 'DENY'

    # Origines de confiance pour CSRF
    CSRF_TRUSTED_ORIGINS = ['https://hillaprince.onrender.com']

# ══════════════════════════════════════════════════════════════
#  CORS — Cross-Origin Resource Sharing
# ══════════════════════════════════════════════════════════════
if IS_PRODUCTION:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS   = ['https://hillaprince.onrender.com']
    CORS_ALLOW_CREDENTIALS = False
else:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS   = [
        'http://localhost:5173',
        'http://localhost:3000',
        'http://127.0.0.1:5173',
    ]

# ══════════════════════════════════════════════════════════════
#  REST FRAMEWORK — rate limiting API
# ══════════════════════════════════════════════════════════════
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # pas de browsable API en prod
    ],
    # Rate limiting global
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        # Throttles spécifiques définis dans views.py
        'contact': '5/hour',
        'cv_download': '10/hour',
    },
}

# ══════════════════════════════════════════════════════════════
#  FICHIERS STATIQUES
# ══════════════════════════════════════════════════════════════
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

REACT_ASSETS_DIR = BASE_DIR / 'react_assets'
STATICFILES_DIRS = [REACT_ASSETS_DIR] if REACT_ASSETS_DIR.exists() else []
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ══════════════════════════════════════════════════════════════
#  INTERNATIONALISATION
# ══════════════════════════════════════════════════════════════
LANGUAGE_CODE      = 'fr-fr'
TIME_ZONE          = 'Africa/Ndjamena'
USE_I18N           = True
USE_TZ             = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ══════════════════════════════════════════════════════════════
#  CKEDITOR 5
# ══════════════════════════════════════════════════════════════
CKEDITOR_5_FILE_STORAGE      = 'api.storage.ArticleImageStorage'
CKEDITOR_5_UPLOAD_FILE_TYPES = ['jpeg', 'jpg', 'png', 'gif', 'webp', 'svg']
CKEDITOR_5_MAX_FILE_SIZE     = 10

CKEDITOR_5_CONFIGS = {
    'article': {
        'toolbar': {
            'items': [
                'heading', '|',
                'bold', 'italic', 'underline', 'strikethrough', '|',
                'fontSize', 'fontColor', 'fontBackgroundColor', '|',
                'link', 'blockQuote', '|',
                'bulletedList', 'numberedList', 'todoList', '|',
                'outdent', 'indent', '|',
                'insertImage', 'insertTable', 'horizontalLine', '|',
                'code', 'codeBlock', '|',
                'sourceEditing', '|',
                'undo', 'redo',
            ],
            'shouldNotGroupWhenFull': True,
        },
        'image': {
            'toolbar': [
                'imageTextAlternative', '|',
                'imageStyle:inline', 'imageStyle:block', 'imageStyle:side',
                'imageStyle:alignLeft', 'imageStyle:alignCenter', 'imageStyle:alignRight',
                '|', 'toggleImageCaption', 'resizeImage',
            ],
            'insert': {'integrations': ['url', 'upload']},
            'resizeOptions': [
                {'name': 'resizeImage:original', 'label': 'Original', 'value': None},
                {'name': 'resizeImage:25',  'label': '25%',  'value': '25'},
                {'name': 'resizeImage:50',  'label': '50%',  'value': '50'},
                {'name': 'resizeImage:75',  'label': '75%',  'value': '75'},
            ],
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraphe', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Titre 1',   'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Titre 2 ★', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Titre 3',   'class': 'ck-heading_heading3'},
                {'model': 'heading4', 'view': 'h4', 'title': 'Titre 4',   'class': 'ck-heading_heading4'},
            ],
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells',
                               'tableProperties', 'tableCellProperties'],
        },
        'codeBlock': {
            'languages': [
                {'language': 'plaintext',  'label': 'Texte brut'},
                {'language': 'python',     'label': 'Python'},
                {'language': 'javascript', 'label': 'JavaScript'},
                {'language': 'typescript', 'label': 'TypeScript'},
                {'language': 'bash',       'label': 'Bash / Shell'},
                {'language': 'yaml',       'label': 'YAML'},
                {'language': 'json',       'label': 'JSON'},
                {'language': 'html',       'label': 'HTML'},
                {'language': 'css',        'label': 'CSS'},
                {'language': 'sql',        'label': 'SQL'},
            ],
        },
        'link':     {'addTargetToExternalLinks': True, 'defaultProtocol': 'https://'},
        'language': 'fr',
        'height':   '650px',
    },
}

# ══════════════════════════════════════════════════════════════
#  LOGGING — monitoring sécurité
# ══════════════════════════════════════════════════════════════
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'secure': {
            'format': '[{levelname}] {asctime} {name} — {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class':     'logging.StreamHandler',
            'formatter': 'secure',
        },
    },
    'loggers': {
        'django.security': {   # tentatives d'intrusion, erreurs CSRF, etc.
            'handlers':  ['console'],
            'level':     'WARNING',
            'propagate': False,
        },
        'django.request': {    # erreurs 4xx et 5xx
            'handlers':  ['console'],
            'level':     'WARNING',
            'propagate': False,
        },
        'django': {
            'handlers':  ['console'],
            'level':     'INFO' if IS_PRODUCTION else 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level':    'WARNING' if IS_PRODUCTION else 'INFO',
    },
}