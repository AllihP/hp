#!/bin/bash
# ================================================================
# PORTFOLIO - Hilla Prince Bambé
# Script d'installation et de démarrage
# Django Backend + React Frontend | FR / EN / AR
# ================================================================

set -e

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}"
echo "  ██╗  ██╗██████╗ ██████╗     ██████╗  ██████╗ ██████╗ ████████╗███████╗ ██████╗ ██╗     ██╗ ██████╗ "
echo "  ██║  ██║██╔══██╗██╔══██╗    ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔═══██╗██║     ██║██╔═══██╗"
echo "  ███████║██████╔╝██████╔╝    ██████╔╝██║   ██║██████╔╝   ██║   █████╗  ██║   ██║██║     ██║██║   ██║"
echo "  ██╔══██║██╔═══╝ ██╔══██╗    ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══╝  ██║   ██║██║     ██║██║   ██║"
echo "  ██║  ██║██║     ██████╔╝    ██║     ╚██████╔╝██║  ██║   ██║   ██║     ╚██████╔╝███████╗██║╚██████╔╝"
echo "  ╚═╝  ╚═╝╚═╝     ╚═════╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚═╝ ╚═════╝ "
echo -e "${NC}"
echo -e "${BLUE}Portfolio — Hilla Prince Bambé | Django + React | FR / EN / AR${NC}"
echo "================================================================"

# ── Backend Setup ─────────────────────────────────────────────
echo -e "\n${YELLOW}[1/4] Installation des dépendances Python (Backend Django)...${NC}"
cd backend
python3 -m venv venv 2>/dev/null || true
source venv/bin/activate
pip install -r requirements.txt -q

echo -e "${YELLOW}[2/4] Migration de la base de données...${NC}"
python manage.py migrate --no-input

echo -e "${YELLOW}[3/4] Chargement des données initiales...${NC}"
python manage.py shell -c "from api.models import Profile; exit(0 if Profile.objects.exists() else 1)" 2>/dev/null || python manage.py loaddata api/fixtures/initial_data.json

# Create superuser if not exists
# Superuser : jamais de mot de passe par défaut.
# Si DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD sont définis → création auto,
# sinon Django demande les identifiants de façon interactive.
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py create_default_superuser
else
    python manage.py createsuperuser
fi

cd ..

# ── Frontend Setup ─────────────────────────────────────────────
echo -e "\n${YELLOW}[4/4] Installation des dépendances Node.js (Frontend React)...${NC}"
cd frontend
npm install --silent
echo -e "${GREEN}✓ Dépendances installées${NC}"
cd ..

echo -e "\n${GREEN}================================================================"
echo "✅ INSTALLATION TERMINÉE!"
echo "================================================================${NC}"
echo ""
echo -e "${BLUE}Démarrer le backend Django:${NC}"
echo "  cd backend && source venv/bin/activate && python manage.py runserver"
echo ""
echo -e "${BLUE}Démarrer le frontend React (dans un autre terminal):${NC}"
echo "  cd frontend && npm run dev"
echo ""
echo -e "${BLUE}Admin Django:${NC} http://localhost:8000/admin/"
echo -e "${BLUE}  Login:${NC} les identifiants saisis à la création du superuser"
echo ""
echo -e "${BLUE}API REST:${NC} http://localhost:8000/api/"
echo -e "${BLUE}Frontend:${NC} http://localhost:5173/"
echo ""
echo -e "${YELLOW}Langues disponibles: 🇫🇷 Français | 🇬🇧 English | 🇸🇦 العربية${NC}"
