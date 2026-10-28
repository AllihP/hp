#!/bin/bash
# Démarre Django + React en parallèle

echo "🚀 Démarrage du Portfolio HPB..."

# Backend
cd backend
source venv/bin/activate 2>/dev/null || true
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!
echo "✅ Backend Django: http://localhost:8000/api/"

# Frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend React: http://localhost:5173/"
echo ""
echo "Admin: http://localhost:8000/admin/ (admin / admin123)"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter les serveurs..."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '🛑 Serveurs arrêtés.'" INT
wait
