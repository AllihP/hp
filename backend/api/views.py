from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse

from .models import Profile, Skill, Education, Experience, Certification, Article, ContactMessage, CVProtege
from .serializers import (
    ProfileSerializer, SkillSerializer, EducationSerializer,
    ExperienceSerializer, CertificationSerializer, ArticleSerializer,
    ContactMessageSerializer
)


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
    return Response(ArticleSerializer(Article.objects.all(), many=True).data)


@api_view(['POST'])
def send_contact(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Message envoyé avec succès!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def download_cv(request):
    """
    POST { "code": "MON_CODE" }
    Code correct  → téléchargement du PDF
    Code incorrect → 403
    """
    code_saisi = (request.data.get('code') or '').strip()

    if not code_saisi:
        return Response({'error': 'Veuillez entrer le code d\'accès.'}, status=400)

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
        return FileResponse(fichier, as_attachment=True, filename=cv.nom_fichier, content_type='application/pdf')
    except Exception:
        return Response({'error': 'Fichier introuvable sur le serveur.'}, status=500)


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'Portfolio API - Hilla Prince Bambé'})
