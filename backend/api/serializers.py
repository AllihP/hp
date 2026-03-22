from rest_framework import serializers
from .models import Profile, Skill, Education, Experience, Certification, Article, ContactMessage


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'icon', 'category', 'read_time', 'published_date', 'order',
            'cover_image', 'cover_image_url',
            'title_fr', 'title_en', 'title_ar',
            'subtitle_fr', 'subtitle_en', 'subtitle_ar',
            'summary_fr', 'summary_en', 'summary_ar',
            'content_fr', 'content_en', 'content_ar',
        ]

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
