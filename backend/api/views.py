from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, Skill, Education, Experience, Certification, Article, ContactMessage
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
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['GET'])
def get_skills(request):
    skills = Skill.objects.all()
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_cv(request):
    education = Education.objects.all()
    experience = Experience.objects.all()
    certifications = Certification.objects.all()
    return Response({
        'education': EducationSerializer(education, many=True).data,
        'experience': ExperienceSerializer(experience, many=True).data,
        'certifications': CertificationSerializer(certifications, many=True).data,
    })


@api_view(['GET'])
def get_articles(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def send_contact(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Message envoyé avec succès!'},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'Portfolio API - Hilla Prince Bambé'})
