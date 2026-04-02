#!/usr/bin/env bash
# ============================================================
# build.sh — Script de build pour Render (Backend Django)
# Render l'exécute automatiquement à chaque déploiement
# ============================================================
set -o errexit   # quitter si une commande échoue

echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "🗄️  Application des migrations..."
python manage.py migrate

echo "🎉 Build terminé !"
