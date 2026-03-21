// Contenu détaillé des articles — structure: { sections: [{type, title?, content, code?, lang?}] }

export const ARTICLES_CONTENT = {
  1: {
    fr: {
      readTime: '12 min',
      intro: "GitHub Actions est une plateforme d'intégration et de déploiement continu (CI/CD) intégrée directement dans GitHub. Elle permet d'automatiser vos workflows de build, test et déploiement. Dans ce guide complet, nous allons explorer toutes les fonctionnalités clés avec des exemples pratiques.",
      sections: [
        {
          type: 'heading',
          title: '🔧 Qu\'est-ce que GitHub Actions ?',
          content: "GitHub Actions est un système d'automatisation qui réagit aux événements dans votre dépôt GitHub. Chaque **workflow** est défini dans un fichier YAML et peut être déclenché par des push, pull requests, schedules ou manuellement.\n\nContrairement aux solutions externes comme Jenkins ou CircleCI, GitHub Actions est nativement intégré à votre dépôt — sans configuration d'infrastructure supplémentaire."
        },
        {
          type: 'code',
          title: '📄 Structure d\'un Workflow basique',
          lang: 'yaml',
          code: `name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Run tests
        run: npm test
        
      - name: Build application
        run: npm run build`
        },
        {
          type: 'tip',
          content: "💡 **Astuce Pro :** Utilisez `npm ci` au lieu de `npm install` dans vos workflows CI — il est plus rapide et garantit une installation déterministe basée sur `package-lock.json`."
        },
        {
          type: 'heading',
          title: '🔄 Les Triggers (Événements déclencheurs)',
          content: "GitHub Actions supporte une large variété d'événements déclencheurs. Les plus utilisés sont :\n\n- **push** : déclenché à chaque push sur une branche\n- **pull_request** : lors de la création/mise à jour d'une PR\n- **schedule** : exécution planifiée via cron\n- **workflow_dispatch** : déclenchement manuel\n- **release** : lors de la publication d'une release"
        },
        {
          type: 'code',
          title: '⏰ Workflow avec cron et déclenchement manuel',
          lang: 'yaml',
          code: `on:
  schedule:
    # Chaque jour à 00:00 UTC
    - cron: '0 0 * * *'
  
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environnement cible'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production`
        },
        {
          type: 'heading',
          title: '🚀 Déploiement vers une VM Linux',
          content: "Un cas d'usage très fréquent est le déploiement automatique d'une application vers un serveur. Voici comment déployer une application Django via SSH après chaque merge sur `main`."
        },
        {
          type: 'code',
          title: '🔐 Déploiement SSH automatique',
          lang: 'yaml',
          code: `name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy via SSH
        uses: appleboy/ssh-action@master
        with:
          host: \${{ secrets.SERVER_HOST }}
          username: \${{ secrets.SERVER_USER }}
          key: \${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /var/www/portfolio
            git pull origin main
            source venv/bin/activate
            pip install -r requirements.txt
            python manage.py migrate
            python manage.py collectstatic --noinput
            sudo systemctl restart gunicorn`
        },
        {
          type: 'warning',
          content: "⚠️ **Sécurité :** Ne jamais écrire vos credentials directement dans les fichiers YAML. Utilisez toujours les **GitHub Secrets** (Settings → Secrets → Actions) pour stocker vos clés SSH, tokens et mots de passe."
        },
        {
          type: 'heading',
          title: '📦 Matrices de test (Matrix Strategy)',
          content: "La stratégie de matrice permet de tester votre code sur plusieurs versions de Node.js, Python ou OS simultanément — en parallèle, sans effort supplémentaire."
        },
        {
          type: 'code',
          title: '🧪 Tests sur multiple versions Python',
          lang: 'yaml',
          code: `jobs:
  test:
    runs-on: \${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python \${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: \${{ matrix.python-version }}
          
      - name: Install & Test
        run: |
          pip install -r requirements.txt
          pytest --cov=. --cov-report=xml`
        },
        {
          type: 'conclusion',
          title: '🎯 Conclusion',
          content: "GitHub Actions est un outil extrêmement puissant pour automatiser votre cycle de développement. Avec les concepts présentés dans ce guide — workflows, triggers, matrices, secrets et déploiements — vous avez toutes les clés pour construire des pipelines CI/CD professionnels directement dans votre dépôt GitHub.\n\nLa prochaine étape ? Explorez le **GitHub Actions Marketplace** qui contient des milliers d'actions préconstruites pour Docker, AWS, GCP, Azure et bien plus encore."
        }
      ]
    },
    en: {
      readTime: '12 min',
      intro: "GitHub Actions is a CI/CD platform built directly into GitHub. It lets you automate your build, test, and deployment workflows. In this complete guide, we'll explore all key features with practical examples.",
      sections: [
        {
          type: 'heading',
          title: '🔧 What is GitHub Actions?',
          content: "GitHub Actions is an automation system that reacts to events in your GitHub repository. Each **workflow** is defined in a YAML file and can be triggered by pushes, pull requests, schedules, or manually.\n\nUnlike external solutions like Jenkins or CircleCI, GitHub Actions is natively integrated into your repository — with no additional infrastructure setup."
        },
        {
          type: 'code',
          title: '📄 Basic Workflow Structure',
          lang: 'yaml',
          code: `name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
      - run: npm run build`
        },
        {
          type: 'tip',
          content: "💡 **Pro Tip:** Use `npm ci` instead of `npm install` in CI workflows — it's faster and ensures a deterministic install from `package-lock.json`."
        },
        {
          type: 'conclusion',
          title: '🎯 Conclusion',
          content: "GitHub Actions is an extremely powerful tool for automating your development cycle. With workflows, triggers, matrices, secrets and deployments, you have all the keys to build professional CI/CD pipelines directly in your GitHub repository."
        }
      ]
    },
    ar: {
      readTime: '١٢ دقيقة',
      intro: "GitHub Actions هي منصة CI/CD مدمجة مباشرة في GitHub. تتيح لك أتمتة سير عمل البناء والاختبار والنشر. في هذا الدليل الشامل، سنستكشف جميع الميزات الرئيسية مع أمثلة عملية.",
      sections: [
        {
          type: 'heading',
          title: '🔧 ما هو GitHub Actions؟',
          content: "GitHub Actions هو نظام أتمتة يتفاعل مع الأحداث في مستودع GitHub الخاص بك. كل **سير عمل** محدد في ملف YAML ويمكن تشغيله عن طريق push أو pull requests أو جداول زمنية أو يدويًا."
        },
        {
          type: 'code',
          title: '📄 هيكل سير العمل الأساسي',
          lang: 'yaml',
          code: `name: CI Pipeline
on:
  push:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test`
        },
        {
          type: 'conclusion',
          title: '🎯 الخلاصة',
          content: "GitHub Actions أداة قوية جداً لأتمتة دورة التطوير الخاصة بك. مع مفاهيم سير العمل والمحفزات والأسرار والنشر، لديك جميع المفاتيح لبناء مسارات CI/CD احترافية."
        }
      ]
    }
  },

  2: {
    fr: {
      readTime: '10 min',
      intro: "Red Hat Enterprise Linux (RHEL) est l'une des distributions Linux les plus utilisées en entreprise. Dans ce guide, nous verrons comment intégrer RHEL dans vos pipelines GitHub Actions pour tester, builder et déployer sur des environnements Red Hat.",
      sections: [
        {
          type: 'heading',
          title: '🎩 Pourquoi Red Hat dans GitHub Actions ?',
          content: "De nombreuses entreprises déploient leurs applications sur des serveurs RHEL ou CentOS Stream. Il est donc crucial de tester vos applications dans un environnement Red Hat avant de déployer en production.\n\nGitHub Actions propose des runners `ubuntu-latest` par défaut, mais vous pouvez utiliser des **containers Docker** Red Hat pour simuler votre environnement cible."
        },
        {
          type: 'code',
          title: '🐳 Utiliser un container Red Hat UBI',
          lang: 'yaml',
          code: `name: Test on Red Hat UBI

on: [push]

jobs:
  test-rhel:
    runs-on: ubuntu-latest
    container:
      image: registry.access.redhat.com/ubi9/ubi:latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Install dependencies
        run: |
          dnf install -y python3 python3-pip
          pip3 install -r requirements.txt
          
      - name: Run tests
        run: python3 -m pytest tests/`
        },
        {
          type: 'tip',
          content: "💡 **Red Hat UBI (Universal Base Image)** est disponible gratuitement sur le Red Hat Container Registry. C'est l'image de base officielle compatible RHEL, idéale pour les pipelines CI/CD."
        },
        {
          type: 'heading',
          title: '📦 Gestion des paquets avec DNF',
          content: "Sur RHEL 8+, DNF remplace YUM comme gestionnaire de paquets. Voici les commandes essentielles à connaître pour vos scripts d'automatisation."
        },
        {
          type: 'code',
          title: '🔧 Script de déploiement RHEL complet',
          lang: 'bash',
          code: `#!/bin/bash
# Script de déploiement pour RHEL/CentOS Stream

set -e

echo "🚀 Démarrage du déploiement sur RHEL..."

# Mise à jour du système
dnf update -y

# Installation des dépendances
dnf install -y \\
  python3 \\
  python3-pip \\
  nginx \\
  postgresql-server

# Déploiement de l'application
cd /opt/app
git pull origin main
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic --noinput

# Redémarrage des services
systemctl restart gunicorn
systemctl reload nginx

echo "✅ Déploiement terminé avec succès!"`
        },
        {
          type: 'conclusion',
          title: '🎯 Conclusion',
          content: "Intégrer Red Hat dans vos pipelines GitHub Actions vous permet de garantir la compatibilité de votre application avec les environnements RHEL en production. L'utilisation des images UBI permet de faire cela sans licence Red Hat supplémentaire."
        }
      ]
    },
    en: {
      readTime: '10 min',
      intro: "Red Hat Enterprise Linux (RHEL) is one of the most widely used Linux distributions in enterprise environments. In this guide, we'll see how to integrate RHEL into your GitHub Actions pipelines.",
      sections: [
        { type: 'heading', title: '🎩 Why Red Hat in GitHub Actions?', content: "Many companies deploy their applications on RHEL or CentOS Stream servers. Testing in a Red Hat environment before deploying to production is crucial." },
        { type: 'code', title: '🐳 Using Red Hat UBI Container', lang: 'yaml', code: `name: Test on Red Hat UBI\non: [push]\njobs:\n  test-rhel:\n    runs-on: ubuntu-latest\n    container:\n      image: registry.access.redhat.com/ubi9/ubi:latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: dnf install -y python3 python3-pip\n      - run: pip3 install -r requirements.txt\n      - run: python3 -m pytest tests/` },
        { type: 'conclusion', title: '🎯 Conclusion', content: "Integrating Red Hat into your GitHub Actions pipelines guarantees compatibility with RHEL production environments." }
      ]
    },
    ar: {
      readTime: '١٠ دقائق',
      intro: "Red Hat Enterprise Linux (RHEL) هو أحد أكثر توزيعات Linux استخدامًا في بيئات المؤسسات. في هذا الدليل، سنرى كيفية دمجه في مسارات GitHub Actions.",
      sections: [
        { type: 'heading', title: '🎩 لماذا Red Hat في GitHub Actions؟', content: "تنشر العديد من الشركات تطبيقاتها على خوادم RHEL. الاختبار في بيئة Red Hat قبل النشر في الإنتاج أمر بالغ الأهمية." },
        { type: 'conclusion', title: '🎯 الخلاصة', content: "يضمن دمج Red Hat في مسارات GitHub Actions التوافق مع بيئات الإنتاج RHEL." }
      ]
    }
  },

  3: {
    fr: {
      readTime: '15 min',
      intro: "Azure DevOps et GitHub Actions sont deux plateformes CI/CD puissantes. Dans certains contextes, vous avez besoin de les faire fonctionner ensemble — par exemple, votre code est sur GitHub mais vos pipelines de déploiement sont dans Azure DevOps. Ce guide couvre l'intégration complète.",
      sections: [
        {
          type: 'heading',
          title: '☁️ Architectures d\'intégration possibles',
          content: "Il existe principalement deux patterns d'intégration :\n\n**Pattern 1 — GitHub déclenche Azure DevOps**\nVos devs travaillent sur GitHub → GitHub Actions effectue les tests → Appelle Azure DevOps Pipeline pour le déploiement.\n\n**Pattern 2 — Azure DevOps surveille GitHub**\nAzure DevOps Pipeline est configuré pour surveiller un dépôt GitHub et se déclenche automatiquement."
        },
        {
          type: 'code',
          title: '🔗 Déclencher Azure DevOps depuis GitHub Actions',
          lang: 'yaml',
          code: `name: Trigger Azure DevOps Pipeline

on:
  push:
    branches: [ main ]

jobs:
  trigger-azure:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Azure Pipeline
        run: |
          curl -X POST \\
            -H "Content-Type: application/json" \\
            -H "Authorization: Basic \$(echo -n ':\${{ secrets.AZURE_PAT }}' | base64)" \\
            "https://dev.azure.com/{org}/{project}/_apis/build/builds?api-version=7.0" \\
            -d '{
              "definition": { "id": 1 },
              "sourceBranch": "refs/heads/main",
              "parameters": "{\\"environment\\":\\"production\\"}"
            }'`
        },
        {
          type: 'warning',
          content: "⚠️ **Important :** Le Personal Access Token (PAT) Azure DevOps doit avoir les permissions **Build (Read & Execute)**. Stockez-le impérativement dans les GitHub Secrets."
        },
        {
          type: 'code',
          title: '🔄 Pipeline Azure DevOps déclenché depuis GitHub',
          lang: 'yaml',
          code: `# azure-pipelines.yml
trigger: none  # Désactiver le trigger automatique

resources:
  repositories:
    - repository: github-repo
      type: github
      endpoint: GitHubConnection
      name: hillaprince/portfolio

pr:
  branches:
    include:
      - main

pool:
  vmImage: ubuntu-latest

steps:
  - checkout: github-repo
  
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.11'
      
  - script: |
      pip install -r requirements.txt
      python manage.py test
    displayName: 'Run Django Tests'
    
  - task: Docker@2
    displayName: 'Build & Push Docker Image'
    inputs:
      command: buildAndPush
      containerRegistry: 'AzureContainerRegistry'
      repository: 'portfolio-hpb'
      tags: |
        \$(Build.BuildId)
        latest`
        },
        {
          type: 'conclusion',
          title: '🎯 Conclusion',
          content: "L'intégration GitHub Actions + Azure DevOps offre le meilleur des deux mondes : la flexibilité de GitHub pour la gestion du code et la puissance d'Azure DevOps pour les déploiements enterprise. Cette approche est particulièrement adaptée aux équipes en migration progressive vers GitHub."
        }
      ]
    },
    en: {
      readTime: '15 min',
      intro: "Azure DevOps and GitHub Actions are two powerful CI/CD platforms. In some contexts, you need them to work together — for example, your code is on GitHub but your deployment pipelines are in Azure DevOps.",
      sections: [
        { type: 'heading', title: '☁️ Integration Architecture', content: "Two main integration patterns exist:\n\n**Pattern 1 — GitHub triggers Azure DevOps:** Devs work on GitHub → Actions run tests → Calls Azure DevOps Pipeline for deployment.\n\n**Pattern 2 — Azure DevOps monitors GitHub:** Azure Pipeline is configured to watch a GitHub repo and triggers automatically." },
        { type: 'code', title: '🔗 Trigger Azure DevOps from GitHub Actions', lang: 'yaml', code: `name: Trigger Azure DevOps\non:\n  push:\n    branches: [ main ]\njobs:\n  trigger:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Trigger Azure Pipeline\n        run: |\n          curl -X POST \\\n            -H "Authorization: Basic $(echo -n ':\${{ secrets.AZURE_PAT }}' | base64)" \\\n            "https://dev.azure.com/{org}/{project}/_apis/build/builds?api-version=7.0" \\\n            -d '{"definition": {"id": 1}}'` },
        { type: 'conclusion', title: '🎯 Conclusion', content: "The GitHub Actions + Azure DevOps integration offers the best of both worlds — GitHub's flexibility and Azure DevOps' enterprise deployment power." }
      ]
    },
    ar: {
      readTime: '١٥ دقيقة',
      intro: "Azure DevOps وGitHub Actions منصتا CI/CD قويتان. في بعض السياقات، تحتاج إلى جعلهما يعملان معًا.",
      sections: [
        { type: 'heading', title: '☁️ معماريات التكامل', content: "هناك نمطان رئيسيان للتكامل: GitHub يشغّل Azure DevOps، أو Azure DevOps يراقب GitHub." },
        { type: 'conclusion', title: '🎯 الخلاصة', content: "يوفر تكامل GitHub Actions مع Azure DevOps أفضل ما في العالمين — مرونة GitHub وقوة Azure DevOps للنشر المؤسسي." }
      ]
    }
  },

  4: {
    fr: {
      readTime: '18 min',
      intro: "PostGIS et GeoServer sont les piliers d'une infrastructure GIS open-source moderne. Dans ce guide basé sur mon expérience au projet ANLA (Surveillance Acridienne), nous verrons comment mettre en place une stack GIS complète et production-ready.",
      sections: [
        {
          type: 'heading',
          title: '🗺️ Stack GIS : Architecture globale',
          content: "Notre stack GIS est composée de :\n\n- **PostgreSQL + PostGIS** : Stockage et requêtes spatiales\n- **GeoServer** : Serveur de tuiles et WMS/WFS\n- **QGIS** : Visualisation et édition desktop\n- **OpenLayers** : Carte web interactive\n- **Flask/Django** : API backend et formulaires de saisie"
        },
        {
          type: 'code',
          title: '🐘 Installation PostGIS sur Ubuntu/Debian',
          lang: 'bash',
          code: `# Installation PostgreSQL + PostGIS
sudo apt-get update
sudo apt-get install -y postgresql-15 postgresql-15-postgis-3

# Créer la base de données spatiale
sudo -u postgres psql << EOF
CREATE DATABASE gis_anla;
\\c gis_anla
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
CREATE EXTENSION fuzzystrmatch;
CREATE EXTENSION postgis_tiger_geocoder;

-- Vérification
SELECT PostGIS_version();
EOF`
        },
        {
          type: 'code',
          title: '📥 Import de données shapefile avec ogr2ogr',
          lang: 'bash',
          code: `# Import d'un shapefile de zones administratives
ogr2ogr \\
  -f "PostgreSQL" \\
  PG:"dbname=gis_anla user=postgres password=secret" \\
  zones_tchad.shp \\
  -nln zones_administratives \\
  -t_srs EPSG:4326 \\
  -overwrite \\
  -progress

# Vérification de l'import
psql -d gis_anla -c "SELECT COUNT(*), ST_Extent(wkb_geometry) FROM zones_administratives;"`
        },
        {
          type: 'tip',
          content: "💡 **Expérience terrain :** Sur le projet ANLA, nous avons importé plus de 50 000 points GPS de surveillance acridienne avec des scripts d'import incrémental qui tournent toutes les heures pour garder les données à jour en temps réel."
        },
        {
          type: 'code',
          title: '🌐 API Flask pour saisie de données terrain',
          lang: 'python',
          code: `from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_GeomFromText

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/gis_anla'
db = SQLAlchemy(app)

class ObservationLocust(db.Model):
    __tablename__ = 'observations'
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String(50))
    date_obs = db.Column(db.DateTime)
    densite = db.Column(db.Float)  # individus/m²
    superficie = db.Column(db.Float)  # hectares
    geom = db.Column(Geometry('POINT', srid=4326))

@app.post('/api/observations')
def add_observation():
    data = request.json
    obs = ObservationLocust(
        agent_id=data['agent_id'],
        densite=data['densite'],
        superficie=data['superficie'],
        geom=ST_GeomFromText(
            f"POINT({data['longitude']} {data['latitude']})", 4326
        )
    )
    db.session.add(obs)
    db.session.commit()
    return jsonify({'id': obs.id, 'status': 'created'}), 201`
        },
        {
          type: 'conclusion',
          title: '🎯 Conclusion',
          content: "Une infrastructure GIS complète avec PostGIS, GeoServer et une API Flask/Django offre une solution robuste et scalable pour la gestion des données géospatiales. Cette stack est en production sur le projet ANLA de surveillance acridienne au Tchad, traitant des milliers de points GPS quotidiennement."
        }
      ]
    },
    en: {
      readTime: '18 min',
      intro: "PostGIS and GeoServer are the pillars of a modern open-source GIS infrastructure. In this guide based on my experience at the ANLA project (Locust Surveillance), we'll set up a complete, production-ready GIS stack.",
      sections: [
        { type: 'heading', title: '🗺️ GIS Stack Architecture', content: "Our GIS stack consists of:\n\n- **PostgreSQL + PostGIS**: Spatial storage and queries\n- **GeoServer**: Tile server and WMS/WFS\n- **OpenLayers**: Interactive web map\n- **Flask/Django**: Backend API and data entry forms" },
        { type: 'code', title: '🐘 PostGIS Installation', lang: 'bash', code: `sudo apt-get install -y postgresql-15 postgresql-15-postgis-3\nsudo -u postgres psql -c "CREATE DATABASE gis_anla;"\nsudo -u postgres psql -d gis_anla -c "CREATE EXTENSION postgis;"` },
        { type: 'conclusion', title: '🎯 Conclusion', content: "A complete GIS infrastructure with PostGIS, GeoServer, and a Flask/Django API provides a robust, scalable solution for geospatial data management." }
      ]
    },
    ar: {
      readTime: '١٨ دقيقة',
      intro: "PostGIS وGeoServer هما ركيزتا البنية التحتية لنظام المعلومات الجغرافية الحديث. في هذا الدليل المبني على تجربتي في مشروع ANLA لمراقبة الجراد.",
      sections: [
        { type: 'heading', title: '🗺️ معمارية نظام GIS', content: "يتكون نظامنا من: PostgreSQL + PostGIS للتخزين المكاني، وGeoServer لخادم الخرائط، وOpenLayers للخريطة التفاعلية على الويب." },
        { type: 'conclusion', title: '🎯 الخلاصة', content: "توفر البنية التحتية الكاملة لـ GIS مع PostGIS وGeoServer حلاً قوياً وقابلاً للتوسع لإدارة البيانات الجيومكانية." }
      ]
    }
  },

  5: {
    fr: {
      readTime: '14 min',
      intro: "Django REST Framework (DRF) est l'outil de référence pour construire des APIs REST robustes avec Django. Ce guide couvre les patterns avancés : authentication JWT, permissions personnalisées, serializers imbriqués et optimisation des performances.",
      sections: [
        {
          type: 'heading',
          title: '🏗️ Architecture d\'une API DRF avancée',
          content: "Une API REST de production avec DRF suit généralement cette structure :\n\n- **Models** → ORM Django + logique métier\n- **Serializers** → Validation + transformation des données\n- **ViewSets** → CRUD automatique via Router\n- **Permissions** → Contrôle d'accès granulaire\n- **Filters** → Recherche et filtrage\n- **Pagination** → Gestion des grandes collections"
        },
        {
          type: 'code',
          title: '🔐 Authentication JWT avec Simple JWT',
          lang: 'python',
          code: `# settings.py
INSTALLED_APPS = ['rest_framework', 'rest_framework_simplejwt']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}`
        },
        {
          type: 'code',
          title: '⚡ ViewSet optimisé avec select_related',
          lang: 'python',
          code: `from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'published']
    search_fields = ['title_fr', 'title_en', 'content_fr']
    ordering_fields = ['created_at', 'views_count']
    
    def get_queryset(self):
        # Optimisation N+1 avec select_related
        return Article.objects.select_related('author') \\
                              .prefetch_related('tags') \\
                              .filter(is_active=True)
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        article = self.get_object()
        Article.objects.filter(pk=pk).update(views_count=F('views_count') + 1)
        return Response({'views': article.views_count + 1})`
        },
        {
          type: 'tip',
          content: "💡 **Performance :** Toujours utiliser `select_related()` pour les ForeignKeys et `prefetch_related()` pour les ManyToMany. Cela évite le problème N+1 et peut réduire les requêtes SQL de 90%."
        },
        {
          type: 'conclusion',
          title: '🎯 Conclusion',
          content: "Django REST Framework offre une base solide pour construire des APIs professionnelles. En maîtrisant les ViewSets, la pagination, l'optimisation des requêtes et l'authentification JWT, vous pouvez construire des APIs capables de gérer des milliers de requêtes par seconde."
        }
      ]
    },
    en: {
      readTime: '14 min',
      intro: "Django REST Framework (DRF) is the go-to tool for building robust REST APIs with Django. This guide covers advanced patterns: JWT authentication, custom permissions, nested serializers, and performance optimization.",
      sections: [
        { type: 'heading', title: '🏗️ Advanced DRF API Architecture', content: "A production REST API with DRF follows this structure:\n\n- **Models** → Django ORM + business logic\n- **Serializers** → Data validation + transformation\n- **ViewSets** → Automatic CRUD via Router\n- **Permissions** → Granular access control" },
        { type: 'code', title: '🔐 JWT Authentication', lang: 'python', code: `REST_FRAMEWORK = {\n    'DEFAULT_AUTHENTICATION_CLASSES': [\n        'rest_framework_simplejwt.authentication.JWTAuthentication',\n    ],\n    'DEFAULT_PERMISSION_CLASSES': [\n        'rest_framework.permissions.IsAuthenticated',\n    ],\n}` },
        { type: 'conclusion', title: '🎯 Conclusion', content: "Django REST Framework provides a solid foundation for building professional APIs. By mastering ViewSets, JWT auth, and query optimization, you can build APIs handling thousands of requests per second." }
      ]
    },
    ar: {
      readTime: '١٤ دقيقة',
      intro: "Django REST Framework هو الأداة المرجعية لبناء واجهات برمجة REST قوية مع Django. يغطي هذا الدليل الأنماط المتقدمة: مصادقة JWT والأذونات المخصصة وتحسين الأداء.",
      sections: [
        { type: 'heading', title: '🏗️ معمارية API متقدمة', content: "تتبع واجهة برمجة REST في الإنتاج مع DRF هذا الهيكل: النماذج، والمسلسلات، وViewSets، والأذونات." },
        { type: 'conclusion', title: '🎯 الخلاصة', content: "يوفر Django REST Framework أساساً متيناً لبناء واجهات برمجة احترافية قادرة على التعامل مع آلاف الطلبات في الثانية." }
      ]
    }
  },

  6: {
    fr: {
      readTime: '16 min',
      intro: "L'intégration de l'IA dans vos applications n'a jamais été aussi accessible. L'API Anthropic (Claude) offre des capacités de raisonnement avancées que vous pouvez intégrer dans vos projets Python et Django en quelques lignes de code. Ce guide couvre mon package kiceko_ai développé pour KICEKO CONSULTANT.",
      sections: [
        {
          type: 'heading',
          title: '🤖 Pourquoi Claude d\'Anthropic ?',
          content: "Parmi les modèles disponibles, Claude se distingue par :\n\n- **Raisonnement long** : Capacité à analyser des documents complexes\n- **Sécurité** : Constitutional AI réduit les hallucinations\n- **Contexte large** : Jusqu'à 200 000 tokens\n- **API simple** : Interface REST claire et bien documentée\n- **Coût maîtrisé** : Pricing par token très compétitif"
        },
        {
          type: 'code',
          title: '📦 Installation et configuration',
          lang: 'python',
          code: `# Installation
pip install anthropic

# Configuration (settings.py pour Django)
import anthropic

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

# Client singleton
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)`
        },
        {
          type: 'code',
          title: '🧠 Module AI pour analyse de projets (kiceko_ai)',
          lang: 'python',
          code: `# kiceko_ai/project_analyzer.py
import anthropic
from django.conf import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

def analyze_project_risks(project_description: str, budget: float) -> dict:
    """
    Analyse les risques d'un projet IT avec Claude.
    Utilisé pour les offres Banque Mondiale et PNUD.
    """
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        system="""Tu es un expert en gestion de projets IT pour l'Afrique subsaharienne.
        Analyse les risques et fournis une réponse en JSON structuré avec:
        - risks: liste des risques identifiés (niveau: LOW/MEDIUM/HIGH)
        - mitigation: stratégies de mitigation
        - budget_adequacy: évaluation du budget (INSUFFICIENT/ADEQUATE/COMFORTABLE)
        - recommendations: liste de recommandations""",
        messages=[{
            "role": "user",
            "content": f"Projet: {project_description}\\nBudget: {budget} USD"
        }]
    )
    
    import json
    return json.loads(message.content[0].text)

# Utilisation
result = analyze_project_risks(
    "Déploiement d'un système GIS pour surveillance acridienne au Sahel",
    budget=150000
)
print(f"Risques identifiés: {len(result['risks'])}")
print(f"Budget: {result['budget_adequacy']}")`
        },
        {
          type: 'code',
          title: '⚡ Streaming pour les réponses longues',
          lang: 'python',
          code: `from django.http import StreamingHttpResponse
import anthropic

def stream_ai_response(request):
    """Vue Django pour streamer une réponse Claude."""
    prompt = request.GET.get('prompt', '')
    
    def generate():
        client = anthropic.Anthropic()
        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {text}\\n\\n"
        yield "data: [DONE]\\n\\n"
    
    return StreamingHttpResponse(
        generate(),
        content_type='text/event-stream'
    )`
        },
        {
          type: 'tip',
          content: "💡 **Expérience KICEKO :** Nous utilisons l'API Claude pour générer automatiquement des sections de propositions techniques pour les appels d'offres Banque Mondiale et PNUD. Cela réduit le temps de rédaction de 60%."
        },
        {
          type: 'conclusion',
          title: '🎯 Conclusion',
          content: "L'intégration de Claude dans vos applications Django ouvre des possibilités infinies : analyse de documents, génération de rapports, assistance à la saisie, chatbots intelligents. Le package kiceko_ai que j'ai développé pour KICEKO CONSULTANT illustre comment encapsuler ces capacités dans des modules métier réutilisables."
        }
      ]
    },
    en: {
      readTime: '16 min',
      intro: "Integrating AI into your applications has never been more accessible. The Anthropic API (Claude) offers advanced reasoning capabilities you can integrate into your Python and Django projects in just a few lines of code.",
      sections: [
        { type: 'heading', title: '🤖 Why Anthropic Claude?', content: "Claude stands out with:\n\n- **Long reasoning**: Ability to analyze complex documents\n- **Safety**: Constitutional AI reduces hallucinations\n- **Large context**: Up to 200,000 tokens\n- **Simple API**: Clear, well-documented REST interface" },
        { type: 'code', title: '📦 Installation & Setup', lang: 'python', code: `pip install anthropic\n\nimport anthropic\nclient = anthropic.Anthropic(api_key="your-api-key")\n\nmessage = client.messages.create(\n    model="claude-opus-4-6",\n    max_tokens=1024,\n    messages=[{"role": "user", "content": "Analyze this project..."}]\n)\nprint(message.content[0].text)` },
        { type: 'conclusion', title: '🎯 Conclusion', content: "Integrating Claude into your Django applications opens infinite possibilities: document analysis, report generation, intelligent chatbots, and automated proposal writing." }
      ]
    },
    ar: {
      readTime: '١٦ دقيقة',
      intro: "لم يكن دمج الذكاء الاصطناعي في تطبيقاتك أسهل من أي وقت مضى. توفر واجهة Anthropic API (Claude) قدرات استدلال متقدمة يمكنك دمجها في مشاريع Python وDjango.",
      sections: [
        { type: 'heading', title: '🤖 لماذا Claude من Anthropic؟', content: "يتميز Claude بـ: الاستدلال الطويل، والسلامة عبر Constitutional AI، والسياق الكبير حتى 200,000 رمز مميز، وواجهة برمجة بسيطة." },
        { type: 'conclusion', title: '🎯 الخلاصة', content: "يفتح دمج Claude في تطبيقات Django إمكانيات لا حصر لها: تحليل الوثائق، وتوليد التقارير، وكتابة المقترحات التلقائية." }
      ]
    }
  }
}
