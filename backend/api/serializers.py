from rest_framework import serializers
from .models import (Profile, Skill, Education, Experience, Certification,
                     Author, Article, ArticleAuthor, ArticleAttachment,
                     ContactMessage)


# ══ Anciens modèles (inchangés) ═══════════════════════════════════
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

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']


# ══ Nouveau système d'articles ═════════════════════════════════════

class AuthorSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id','first_name','last_name','title','affiliation',
                  'email','orcid','country','is_corresponding','photo_url',
                  'bio_fr','bio_en']

    def get_photo_url(self, obj):
        if obj.photo:
            req = self.context.get('request')
            return req.build_absolute_uri(obj.photo.url) if req else obj.photo.url
        return None


class ArticleAuthorSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = ArticleAuthor
        fields = ['author', 'order']


class ArticleAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ArticleAttachment
        fields = ['id','file_url','file_type','description_fr','description_en','uploaded_at']

    def get_file_url(self, obj):
        req = self.context.get('request')
        if req and obj.file:
            return req.build_absolute_uri(obj.file.url)
        return None


class ArticleListSerializer(serializers.ModelSerializer):
    """Version légère pour la grille des articles."""
    og_image_url  = serializers.SerializerMethodField()
    authors_names = serializers.SerializerMethodField()
    keywords      = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id','doi','status','journal_name','volume','year','published_at',
            'title_fr','title_en','title_ar',
            'subtitle_fr','subtitle_en','subtitle_ar',
            'abstract_fr','abstract_en','abstract_ar',
            'keywords_fr','keywords_en','keywords_ar',
            'keywords',
            'og_image_url', 'key_metrics', 'view_count', 'authors_names',
        ]

    def get_og_image_url(self, obj):
        if obj.og_image:
            req = self.context.get('request')
            return req.build_absolute_uri(obj.og_image.url) if req else obj.og_image.url
        return None

    def get_authors_names(self, obj):
        return [str(aa.author) for aa in obj.articleauthor_set.all()[:3]]

    def get_keywords(self, obj):
        """Retourne les mots-clés FR comme liste pour compatibilité frontend."""
        kw = obj.keywords_fr or obj.keywords_en or ''
        return [k.strip() for k in kw.split(',') if k.strip()]


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Version complète pour la page de lecture."""
    og_image_url  = serializers.SerializerMethodField()
    authors       = ArticleAuthorSerializer(many=True, read_only=True, source='articleauthor_set')
    attachments   = ArticleAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id','doi','status','journal_name','volume','year',
            'submitted_at','published_at','updated_at','view_count',
            'og_image_url',
            'title_fr','title_en','title_ar',
            'subtitle_fr','subtitle_en','subtitle_ar',
            'abstract_fr','abstract_en','abstract_ar',
            'keywords_fr','keywords_en','keywords_ar',
            'key_metrics','content_sections','references',
            'meta_description_fr','meta_description_en','meta_description_ar',
            'authors','attachments',
        ]

    def get_og_image_url(self, obj):
        if obj.og_image:
            req = self.context.get('request')
            return req.build_absolute_uri(obj.og_image.url) if req else obj.og_image.url
        return None
