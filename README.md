<<<<<<< HEAD
# 🌟 Portfolio – Hilla Prince Bambé
**Django Backend + React Frontend | Trilingue FR / EN / AR**

---

## ✨ Fonctionnalités

| Feature | Description |
|---------|-------------|
| 🌍 **Trilingue** | Français, English, العربية avec RTL automatique |
| 🎨 **Design hexagonal** | Thème dark navy + gold inspiré du background |
| ⚡ **Animations fluides** | Typewriter, scroll reveal, hexagones flottants |
| 📱 **Responsive** | Mobile, tablette, desktop |
| 🔗 **API REST** | Django REST Framework avec données dynamiques |
| 🧩 **Fallback offline** | Fonctionne sans backend (données statiques) |
| 🔒 **Admin Django** | Gestion du contenu via interface admin |

---

## 🏗️ Architecture

```
portfolio/
├── backend/                    # Django REST API
│   ├── api/
│   │   ├── models.py           # Profile, Skill, Education, Experience, Certification, Article, Contact
│   │   ├── serializers.py      # DRF Serializers
│   │   ├── views.py            # API Views
│   │   ├── urls.py             # API Routes
│   │   ├── admin.py            # Admin interface
│   │   └── fixtures/
│   │       └── initial_data.json  # Données de départ
│   ├── portfolio/
│   │   ├── settings.py
│   │   └── urls.py
│   ├── requirements.txt
│   └── manage.py
│
├── frontend/                   # React + Vite
│   ├── src/
│   │   ├── assets/             # Images (background, hilla, logo)
│   │   ├── components/
│   │   │   ├── Navbar.jsx/.css
│   │   │   ├── Footer.jsx/.css
│   │   │   └── Contact.jsx/.css
│   │   ├── context/
│   │   │   └── LangContext.jsx  # Gestion langue + RTL
│   │   ├── hooks/
│   │   │   └── useApi.js        # Appels API Axios
│   │   ├── i18n/
│   │   │   ├── fr.json          # Traductions FR
│   │   │   ├── en.json          # Traductions EN
│   │   │   ├── ar.json          # Traductions AR
│   │   │   └── index.js         # Config i18next
│   │   ├── pages/
│   │   │   ├── Home.jsx/.css    # Page d'accueil + typewriter
│   │   │   ├── About.jsx/.css   # Compétences + barre de progression
│   │   │   ├── CV.jsx/.css      # Formation, Expérience, Certifications
│   │   │   └── Articles.jsx/.css # Articles filtrables
│   │   ├── styles/
│   │   │   └── global.css       # Variables CSS, animations globales
│   │   ├── App.jsx              # Router + chargement données
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── setup.sh                    # Installation automatique
├── start.sh                    # Démarrage des deux serveurs
└── README.md
```

---

## 🚀 Installation

### Option 1 – Script automatique
```bash
chmod +x setup.sh && ./setup.sh
```

### Option 2 – Manuelle

**Backend Django:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata api/fixtures/initial_data.json
python manage.py runserver
```

**Frontend React (nouveau terminal):**
```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 URLs

| Service | URL |
|---------|-----|
| Frontend React | http://localhost:5173/ |
| API Django | http://localhost:8000/api/ |
| Admin Django | http://localhost:8000/admin/ |
| **Admin login** | `admin` / `admin123` |

---

## 📡 Endpoints API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/` | Health check |
| GET | `/api/profile/` | Profil complet |
| GET | `/api/skills/` | Compétences |
| GET | `/api/cv/` | Formation, Expérience, Certifications |
| GET | `/api/articles/` | Articles |
| POST | `/api/contact/` | Envoyer un message |

---

## 🎨 Design System

```css
--gold:       #f5c518   /* Couleur accent principale */
--navy:       #0a0f1e   /* Fond principal */
--navy-mid:   #111827   /* Fond sections alternées */
--navy-card:  #141c2e   /* Cartes */
--font-display: 'Cinzel', serif     /* Titres */
--font-body:    'Rajdhani', sans-serif  /* Corps de texte */
--font-arabic:  'Cairo', sans-serif     /* Texte arabe */
```

---

## 🌍 Système de traduction

Les données de l'API Django sont stockées en 3 langues :
- `title_fr` / `title_en` / `title_ar`
- `description_fr` / `description_en` / `description_ar`

Le hook `getField(obj, lang, field)` extrait automatiquement la bonne langue.

Le changement EN → AR bascule automatiquement le document en **mode RTL**.

---

## 🛠️ Technologies

**Backend:** Django 4.2 • DRF 3.14 • SQLite (→ PostgreSQL en prod) • CORS Headers

**Frontend:** React 18 • Vite 5 • React Router 6 • React i18next • Framer Motion • Axios • React Intersection Observer

---

## 📦 Production

```bash
# Build frontend
cd frontend && npm run build

# Servir les fichiers statiques depuis Django
# Configurer STATIC_ROOT et collectstatic
cd backend && python manage.py collectstatic

# Utiliser gunicorn + nginx en production
gunicorn portfolio.wsgi:application --bind 0.0.0.0:8000
```

---

*© 2025 Hilla Prince Bambé – KICEKO CONSULTANT, N'Djamena, Tchad*
=======
# hp
portfolio
>>>>>>> 910a0a2fa587c28cbb4f00e70ede2b6ccf42c066
