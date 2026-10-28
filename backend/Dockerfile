# ============================================================
# Dockerfile — Backend Django Portfolio HPB
# Python 3.11 (stable, compatible Django 5.2 + ckeditor-5)
# ============================================================

# ── Image de base — Python 3.11 slim ─────────────────────────
FROM python:3.11-slim

# ── Variables d'environnement ─────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ── Dossier de travail ────────────────────────────────────────
WORKDIR /app

# ── Dépendances système (pour psycopg2, Pillow) ───────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# ── Copier et installer les dépendances Python ────────────────
# (séparé du code source pour profiter du cache Docker)
COPY requirements.txt .
RUN pip install -r requirements.txt

# ── Copier le code source ─────────────────────────────────────
COPY . .

# ── Collecte des fichiers statiques ──────────────────────────
RUN python manage.py collectstatic --noinput \
    --settings=portfolio.settings_prod 2>/dev/null || true

# ── Port exposé ───────────────────────────────────────────────
EXPOSE 8000

# ── Commande de démarrage ─────────────────────────────────────
CMD ["gunicorn", "portfolio.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--timeout", "120", \
     "--log-level", "info"]
