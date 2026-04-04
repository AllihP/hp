from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from django.db.models import Q
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

from .models import (Profile, Skill, Education, Experience, Certification,
                     Article, ContactMessage, CVProtege)
from .serializers import (
    ProfileSerializer, SkillSerializer, EducationSerializer,
    ExperienceSerializer, CertificationSerializer,
    ArticleListSerializer, ArticleDetailSerializer,
    ContactMessageSerializer,
)


# ── Throttles spécifiques ────────────────────────────────────
class ContactThrottle(AnonRateThrottle):
    scope = 'contact'      # 5/hour défini dans settings.py


class CVDownloadThrottle(AnonRateThrottle):
    scope = 'cv_download'  # 10/hour défini dans settings.py


def _clean(text, max_length=500):
    """Nettoie le texte : supprime HTML/JS, limite la longueur."""
    if not text:
        return ''
    # Supprime toutes les balises HTML et attributs dangereux
    text = re.sub(r'<[^>]+>', '', str(text))
    # Supprime les séquences javascript:
    text = re.sub(r'javascript\s*:', '', text, flags=re.IGNORECASE)
    # Supprime les caractères de contrôle
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return text.strip()[:max_length]


# ── Endpoints ────────────────────────────────────────────────

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'service': 'Portfolio HPB — API'})


@api_view(['GET'])
def get_profile(request):
    profile = Profile.objects.first()
    if not profile:
        return Response({'error': 'Profile not found'}, status=404)
    return Response(ProfileSerializer(profile).data)


@api_view(['GET'])
def get_skills(request):
    return Response(SkillSerializer(Skill.objects.all(), many=True).data)


@api_view(['GET'])
def get_cv(request):
    return Response({
        'education':      EducationSerializer(Education.objects.all(), many=True).data,
        'experience':     ExperienceSerializer(Experience.objects.all(), many=True).data,
        'certifications': CertificationSerializer(Certification.objects.all(), many=True).data,
    })


@api_view(['GET'])
def get_articles(request):
    qs = Article.objects.filter(status='published')

    search = _clean(request.query_params.get('search', ''), max_length=100)
    if search:
        qs = qs.filter(
            Q(title_fr__icontains=search) | Q(title_en__icontains=search) |
            Q(abstract_fr__icontains=search) | Q(keywords_fr__icontains=search)
        )

    year = request.query_params.get('year', '').strip()
    if year and year.isdigit() and 2000 <= int(year) <= 2100:
        qs = qs.filter(year=int(year))

    return Response(
        ArticleListSerializer(qs, many=True, context={'request': request}).data
    )


@api_view(['GET'])
def get_article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk, status='published')
    except Article.DoesNotExist:
        return Response({'error': 'Article introuvable.'}, status=404)
    Article.objects.filter(pk=pk).update(view_count=article.view_count + 1)
    return Response(
        ArticleDetailSerializer(article, context={'request': request}).data
    )


@api_view(['GET'])
def get_article_by_doi(request):
    """GET /api/articles/by_doi/?doi=10.xxxx/..."""
    doi = _clean(request.query_params.get('doi', ''), 150)
    if not doi:
        return Response({'error': 'Paramètre doi requis.'}, status=400)
    try:
        article = Article.objects.get(doi=doi, status='published')
    except Article.DoesNotExist:
        return Response({'error': 'Article introuvable.'}, status=404)
    Article.objects.filter(pk=article.pk).update(view_count=article.view_count + 1)
    return Response(
        ArticleDetailSerializer(article, context={'request': request}).data
    )


@api_view(['GET'])
def get_related_articles(request, pk):
    try:
        Article.objects.get(pk=pk, status='published')
    except Article.DoesNotExist:
        return Response([])
    related = Article.objects.filter(status='published').exclude(pk=pk)[:4]
    return Response(
        ArticleListSerializer(related, many=True, context={'request': request}).data
    )


@api_view(['POST'])
@throttle_classes([ContactThrottle])
def send_contact(request):
    """
    Endpoint contact sécurisé :
    - Throttle : 5 messages max/heure par IP
    - Validation stricte de chaque champ
    - Nettoyage XSS de tous les inputs
    - Longueurs limitées
    """
    data = request.data

    # Nettoyage + limitation longueur
    name    = _clean(data.get('name',    ''), 100)
    email   = _clean(data.get('email',   ''), 254)
    subject = _clean(data.get('subject', ''), 200)
    message = _clean(data.get('message', ''), 5000)

    errors = {}

    if not name or len(name) < 2:
        errors['name'] = 'Le nom doit contenir au moins 2 caractères.'

    try:
        validate_email(email)
    except ValidationError:
        errors['email'] = 'Adresse email invalide.'

    if not subject or len(subject) < 3:
        errors['subject'] = 'Le sujet doit contenir au moins 3 caractères.'

    if not message or len(message) < 10:
        errors['message'] = 'Le message doit contenir au moins 10 caractères.'

    if errors:
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

    ContactMessage.objects.create(
        name=name, email=email, subject=subject, message=message
    )

    return Response(
        {'message': 'Message envoyé avec succès !'},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
@throttle_classes([CVDownloadThrottle])
def download_cv(request):
    """
    Téléchargement CV sécurisé :
    - Throttle : 10 tentatives max/heure par IP
    - Validation du code (longueur max, nettoyage)
    - Pas de message d'erreur révélant l'existence ou non du code
    """
    code_saisi = _clean(str(request.data.get('code', '')), 100)

    if not code_saisi:
        return Response({'error': "Veuillez entrer le code d'accès."}, status=400)

    cv = CVProtege.objects.filter(actif=True).first()
    if not cv:
        return Response({'error': 'CV non disponible pour le moment.'}, status=404)

    if code_saisi.lower() != cv.code.strip().lower():
        # Message générique — ne révèle pas si le code est proche ou non
        return Response({'error': 'Code incorrect.'}, status=403)

    try:
        fichier = cv.fichier.open('rb')
        return FileResponse(
            fichier,
            as_attachment=True,
            filename=cv.nom_fichier,
            content_type='application/pdf'
        )
    except Exception:
        return Response({'error': 'Fichier introuvable.'}, status=500)