# ============================================================
# Makefile — Raccourcis commandes Docker
# Usage : make <commande>
# ============================================================

.PHONY: up down build logs shell migrate import createsuperuser

# ── Démarrer tout le stack ────────────────────────────────────
up:
	docker compose up

# ── Démarrer en arrière-plan ──────────────────────────────────
up-d:
	docker compose up -d

# ── Arrêter ───────────────────────────────────────────────────
down:
	docker compose down

# ── Reconstruire les images (après modif requirements.txt) ────
build:
	docker compose build --no-cache

# ── Logs en temps réel ────────────────────────────────────────
logs:
	docker compose logs -f backend

# ── Shell Django ──────────────────────────────────────────────
shell:
	docker compose exec backend python manage.py shell

# ── Migrations ────────────────────────────────────────────────
migrate:
	docker compose exec backend python manage.py migrate

# ── Importer l'article routier ────────────────────────────────
import:
	docker compose exec backend python manage.py import_article --force

# ── Créer un superuser ────────────────────────────────────────
createsuperuser:
	docker compose exec backend python manage.py createsuperuser

# ── Tout réinitialiser (⚠️ supprime les données) ──────────────
reset:
	docker compose down -v
	docker compose up --build
