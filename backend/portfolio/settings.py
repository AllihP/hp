from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-portfolio-hpb-2025'
DEBUG = True
ALLOWED_HOSTS = ['*']

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

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Ndjamena'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
}

# ── CKEditor 5 ────────────────────────────────────────────────
CKEDITOR_5_FILE_STORAGE = 'api.storage.ArticleImageStorage'
CKEDITOR_5_UPLOAD_FILE_TYPES = ['jpeg', 'jpg', 'png', 'gif', 'webp', 'svg']
CKEDITOR_5_MAX_FILE_SIZE = 10

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
                {'model': 'paragraph',                    'title': 'Paragraphe',  'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1',      'title': 'Titre 1',     'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2',      'title': 'Titre 2 ★',   'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3',      'title': 'Titre 3',     'class': 'ck-heading_heading3'},
                {'model': 'heading4', 'view': 'h4',      'title': 'Titre 4',     'class': 'ck-heading_heading4'},
            ],
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells', 'tableProperties', 'tableCellProperties'],
        },
        'codeBlock': {
            'languages': [
                {'language': 'plaintext',   'label': 'Texte brut'},
                {'language': 'python',      'label': 'Python'},
                {'language': 'javascript',  'label': 'JavaScript'},
                {'language': 'typescript',  'label': 'TypeScript'},
                {'language': 'bash',        'label': 'Bash / Shell'},
                {'language': 'yaml',        'label': 'YAML'},
                {'language': 'json',        'label': 'JSON'},
                {'language': 'html',        'label': 'HTML'},
                {'language': 'css',         'label': 'CSS'},
                {'language': 'sql',         'label': 'SQL'},
            ],
        },
        'link': {'addTargetToExternalLinks': True, 'defaultProtocol': 'https://'},
        'language': 'fr',
        'height': '650px',
    },
}
