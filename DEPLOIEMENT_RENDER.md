# 🚀 Guide de Déploiement — Portfolio HPB sur Render

## Structure du repo Git attendue

```
portfolio/                  ← racine du repo
├── render.yaml             ← config Render (à la racine)
├── backend/
│   ├── manage.py
│   ├── requirements.txt    ← remplacer par celui fourni
│   ├── build.sh            ← nouveau
│   ├── .env.example        ← nouveau
│   ├── portfolio/
│   │   ├── settings.py
│   │   ├── settings_prod.py  ← nouveau
│   │   └── wsgi.py
│   └── api/
└── frontend/
    ├── package.json
    ├── vite.config.js      ← remplacer par celui fourni
    └── public/
        └── _redirects      ← nouveau
```

---

## ÉTAPE 1 — Préparer le repo Git

```powershell
# Si vous n'avez pas encore de repo Git
cd C:\Users\hilla\OneDrive\Bureau\portfolio
git init
git add .
git commit -m "Initial commit"

# Créer un repo sur GitHub et le connecter
git remote add origin https://github.com/VOTRE-USERNAME/portfolio-hpb.git
git branch -M main
git push -u origin main
```

---

## ÉTAPE 2 — Vérifier settings.py (compatibilité prod)

Ajoutez ces lignes au début de `backend/portfolio/settings.py` :

```python
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()  # charge .env en local
```

---

## ÉTAPE 3 — Installer les dépendances de prod en local

```powershell
cd backend
venv\Scripts\activate
pip install "django>=5.2" gunicorn whitenoise dj-database-url psycopg2-binary python-dotenv
pip freeze > requirements.txt
```

---

## ÉTAPE 4 — Tester le build en local

```powershell
# Tester gunicorn localement
set DJANGO_SETTINGS_MODULE=portfolio.settings
gunicorn portfolio.wsgi:application --bind 0.0.0.0:8000
```

---

## ÉTAPE 5 — Déployer sur Render

### Option A — Via render.yaml (recommandé)

1. Allez sur [render.com](https://render.com) → **New** → **Blueprint**
2. Connectez votre repo GitHub
3. Render détecte `render.yaml` et crée tout automatiquement
4. Cliquez **Apply**

### Option B — Manuel (service par service)

#### Backend (Web Service)

1. Render → **New** → **Web Service**
2. Connectez votre repo GitHub
3. Paramètres :
   - **Root Directory** : `backend`
   - **Runtime** : Python 3
   - **Build Command** : `./build.sh`
   - **Start Command** : `gunicorn portfolio.wsgi:application --bind 0.0.0.0:$PORT --workers 2`
   - **Instance Type** : Free

4. **Environment Variables** (onglet Environment) :

   | Clé | Valeur |
   |-----|--------|
   | `DJANGO_SETTINGS_MODULE` | `portfolio.settings_prod` |
   | `SECRET_KEY` | *(cliquez "Generate")* |
   | `PYTHON_VERSION` | `3.11.9` |
   | `ALLOWED_HOSTS` | `votre-app.onrender.com` |
   | `CORS_ALLOWED_ORIGINS` | `https://votre-frontend.onrender.com` |

#### Base de données PostgreSQL

1. Render → **New** → **PostgreSQL**
2. Nom : `portfolio-hpb-db`, Plan : Free
3. Copiez l'**Internal Database URL**
4. Dans le Web Service → Environment :
   | Clé | Valeur |
   |-----|--------|
   | `DATABASE_URL` | *(collez l'URL interne)* |

#### Frontend (Static Site)

1. Render → **New** → **Static Site**
2. Connectez le même repo
3. Paramètres :
   - **Root Directory** : `frontend`
   - **Build Command** : `npm install && npm run build`
   - **Publish Directory** : `dist`

4. **Environment Variables** :

   | Clé | Valeur |
   |-----|--------|
   | `VITE_API_URL` | `https://votre-api.onrender.com/api` |
   | `NODE_VERSION` | `20` |

---

## ÉTAPE 6 — Après le premier déploiement

```bash
# Depuis le Shell Render (Dashboard → Shell)
python manage.py import_article
python manage.py createsuperuser
```

---

## ⚠️ Points importants

### SQLite → PostgreSQL
Render a un **système de fichiers éphémère** — SQLite est effacé à chaque déploiement.
La migration vers PostgreSQL est obligatoire pour garder vos données.

### Images médias (articles, avatars)
Les fichiers uploadés dans l'admin sont également effacés.
Pour les persister, utilisez **Cloudinary** (gratuit jusqu'à 25 Go) :

```powershell
pip install cloudinary django-cloudinary-storage
```

Puis dans `settings_prod.py`, décommentez la section Cloudinary.

### Plan Free Render
- Le service s'endort après 15 min d'inactivité
- Premier chargement = 30-60 secondes de réveil
- La DB Free est supprimée après 90 jours d'inactivité

### Variables d'environnement frontend
`VITE_API_URL` doit être définie **avant le build** (pas au runtime).
Si vous changez l'URL de l'API, vous devez redéployer le frontend.

---

## URLs finales

| Service | URL |
|---------|-----|
| Frontend | `https://portfolio-hpb.onrender.com` |
| API | `https://portfolio-hpb-api.onrender.com/api` |
| Admin | `https://portfolio-hpb-api.onrender.com/admin` |

---

## Commandes utiles

```bash
# Voir les logs (depuis le Dashboard Render → Logs)

# Créer un superuser (Shell Render)
python manage.py createsuperuser

# Importer l'article routier automatiquement
python manage.py import_article

# Forcer la mise à jour
python manage.py import_article --force

# Vérifier la config
python manage.py check --deploy
```
