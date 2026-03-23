from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from django.db.models import Q

from .models import (Profile, Skill, Education, Experience, Certification,
                     Article, ContactMessage, CVProtege)
from .serializers import (
    ProfileSerializer, SkillSerializer, EducationSerializer,
    ExperienceSerializer, CertificationSerializer,
    ArticleListSerializer, ArticleDetailSerializer,
    ContactMessageSerializer,
)


# ══ Anciens endpoints (inchangés) ════════════════════════════════

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'Portfolio API - Hilla Prince Bambé'})


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


@api_view(['POST'])
def send_contact(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Message envoyé avec succès!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def download_cv(request):
    code_saisi = (request.data.get('code') or '').strip()
    if not code_saisi:
        return Response({'error': "Veuillez entrer le code d'accès."}, status=400)

    cv = CVProtege.objects.filter(actif=True).first()
    if not cv:
        return Response({'error': 'CV non disponible pour le moment.'}, status=404)

    if code_saisi.lower() != cv.code.strip().lower():
        return Response(
            {'error': 'Code incorrect. Contactez Hilla Prince Bambé pour obtenir le code.'},
            status=403
        )
    try:
        fichier = cv.fichier.open('rb')
        return FileResponse(fichier, as_attachment=True,
                            filename=cv.nom_fichier, content_type='application/pdf')
    except Exception:
        return Response({'error': 'Fichier introuvable sur le serveur.'}, status=500)


# ══ Articles — nouveaux endpoints ════════════════════════════════

@api_view(['GET'])
def get_articles(request):
    """
    Liste des articles publiés.
    Paramètres optionnels: ?search=... &year=...
    """
    qs = Article.objects.filter(status='published')

    search = request.query_params.get('search')
    if search:
        qs = qs.filter(
            Q(title_fr__icontains=search) | Q(title_en__icontains=search) |
            Q(abstract_fr__icontains=search) | Q(keywords_fr__icontains=search)
        )

    year = request.query_params.get('year')
    if year:
        qs = qs.filter(year=year)

    serializer = ArticleListSerializer(qs, many=True,
                                       context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def get_article_detail(request, pk):
    """
    Détail complet d'un article par UUID.
    Incrémente le compteur de vues.
    """
    try:
        article = Article.objects.get(pk=pk, status='published')
    except Article.DoesNotExist:
        return Response({'error': 'Article introuvable.'}, status=404)

    # Incrémenter les vues
    Article.objects.filter(pk=pk).update(view_count=article.view_count + 1)

    serializer = ArticleDetailSerializer(article, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def get_article_by_doi(request):
    """
    GET /api/articles/by_doi/?doi=10.xxxx/...
    Récupère un article par son DOI.
    """
    doi = request.query_params.get('doi', '').strip()
    if not doi:
        return Response({'error': 'Paramètre doi requis.'}, status=400)

    try:
        article = Article.objects.get(doi=doi, status='published')
    except Article.DoesNotExist:
        return Response({'error': 'Article introuvable.'}, status=404)

    Article.objects.filter(pk=article.pk).update(view_count=article.view_count + 1)
    serializer = ArticleDetailSerializer(article, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def get_related_articles(request, pk):
    """Articles publiés similaires (même année ou même journal), excluant l'article courant."""
    try:
        article = Article.objects.get(pk=pk, status='published')
    except Article.DoesNotExist:
        return Response([])

    related = Article.objects.filter(status='published').exclude(pk=pk)[:4]
    serializer = ArticleListSerializer(related, many=True, context={'request': request})
    return Response(serializer.data)
