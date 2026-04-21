#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "━━━ ÉTAPE 1 — Build Frontend React ━━━"
cd frontend
npm install
chmod -R +x node_modules/.bin/ 2>/dev/null || true
# base=/static/ dans vite.config.js → assets sous /static/assets/...
VITE_API_URL=/api node node_modules/vite/bin/vite.js build --mode production
echo "  dist/ :"
ls -la dist/
ls -la dist/assets/ | head -8
cd ..

echo "━━━ ÉTAPE 2 — Copie vers backend ━━━"
# index.html → frontend_dist (servi par serve_spa)
rm -rf backend/frontend_dist
mkdir -p backend/frontend_dist
cp frontend/dist/index.html backend/frontend_dist/index.html

# assets React → react_assets (ajouté dans STATICFILES_DIRS)
rm -rf backend/react_assets
mkdir -p backend/react_assets
cp -r frontend/dist/assets backend/react_assets/assets
echo "  index.html copié dans frontend_dist/"
echo "  assets/ copié dans react_assets/ :"
ls backend/react_assets/assets/ | head -5

echo "━━━ ÉTAPE 3 — Dépendances Python ━━━"
cd backend
pip install -r requirements.txt --quiet

echo "━━━ ÉTAPE 4 — Collecte statiques ━━━"
# collectstatic va inclure react_assets/assets/ via STATICFILES_DIRS
python manage.py collectstatic --noinput
echo "  staticfiles/assets/ :"
ls staticfiles/assets/ 2>/dev/null | head -5 || echo "  (vide)"

echo "━━━ ÉTAPE 5 — Migrations ━━━"
python manage.py migrate

echo "━━━ ÉTAPE 6 — Import article + Superuser ━━━"
# On utilise || true pour éviter que le build échoue si l'article n'existe pas encore
# ou si le superuser est déjà créé.
python manage.py import_article || echo "⚠️ Note: Aucun article importé (Base vide ou déjà remplie)"
python manage.py create_default_superuser || echo "⚠️ Note: Le superuser existe déjà ou n'a pas pu être créé"

echo ""
echo "============================================================"
echo "   BUILD TERMINÉ AVEC SUCCÈS 🎉"
echo "============================================================"
