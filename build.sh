#!/usr/bin/env bash
set -o errexit

echo "━━━ ÉTAPE 1 — Build Frontend React ━━━"
cd frontend
npm install --prefer-offline
npx --yes vite build --mode production
cd ..

echo "━━━ ÉTAPE 2 — Copie dist → backend/frontend_dist ━━━"
rm -rf backend/frontend_dist
mkdir -p backend/frontend_dist
cp -r frontend/dist/. backend/frontend_dist/
echo "  ✅ $(ls backend/frontend_dist | wc -l) fichiers copiés"

echo "━━━ ÉTAPE 3 — Dépendances Python ━━━"
cd backend
pip install -r requirements.txt --quiet

echo "━━━ ÉTAPE 4 — Collecte statiques ━━━"
python manage.py collectstatic --noinput

echo "━━━ ÉTAPE 5 — Migrations ━━━"
python manage.py migrate

echo "━━━ ÉTAPE 6 — Import article + Superuser ━━━"
python manage.py import_article
python manage.py create_default_superuser

echo "━━━ 🎉 BUILD TERMINÉ ━━━"
