#!/usr/bin/env bash
set -o errexit

echo "━━━ ÉTAPE 1 — Build Frontend React ━━━"
cd frontend
npm install
chmod -R +x node_modules/.bin/ 2>/dev/null || true
# VITE_API_URL=/api + base=/static/ dans vite.config.js
VITE_API_URL=/api node node_modules/vite/bin/vite.js build --mode production
echo "  dist/ généré :"
ls dist/
cd ..

echo "━━━ ÉTAPE 2 — Copie index.html → backend/frontend_dist ━━━"
rm -rf backend/frontend_dist
mkdir -p backend/frontend_dist
# Copier SEULEMENT index.html ici (les assets iront dans staticfiles)
cp frontend/dist/index.html backend/frontend_dist/index.html
echo "  ✅ index.html copié"

echo "━━━ ÉTAPE 3 — Dépendances Python ━━━"
cd backend
pip install -r requirements.txt --quiet

echo "━━━ ÉTAPE 4 — Collecte statiques Django ━━━"
python manage.py collectstatic --noinput
# Copier les assets React dans staticfiles/
# (Vite les a générés sous dist/assets/ avec base=/static/)
mkdir -p staticfiles/assets
if [ -d "../frontend/dist/assets" ]; then
    cp -r ../frontend/dist/assets/. staticfiles/assets/
    echo "  ✅ Assets React copiés dans staticfiles/assets/"
    ls staticfiles/assets/ | head -5
fi

echo "━━━ ÉTAPE 5 — Migrations ━━━"
python manage.py migrate

echo "━━━ ÉTAPE 6 — Import article + Superuser ━━━"
python manage.py import_article
python manage.py create_default_superuser

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🎉 BUILD TERMINÉ"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
