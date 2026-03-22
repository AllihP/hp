from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Profile(models.Model):
    name_fr = models.CharField(max_length=100, default="Hilla Prince Bambé")
    name_en = models.CharField(max_length=100, default="Hilla Prince Bambé")
    name_ar = models.CharField(max_length=100, default="هيلا برانس بامبي")
    title_fr = models.CharField(max_length=200, default="Ingénieur des Technologies d'Information")
    title_en = models.CharField(max_length=200, default="Information Technology Engineer")
    title_ar = models.CharField(max_length=200, default="مهندس تكنولوجيا المعلومات")
    bio_fr = models.TextField(blank=True, default="")
    bio_en = models.TextField(blank=True, default="")
    bio_ar = models.TextField(blank=True, default="")
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")
    linkedin = models.URLField(blank=True, default="")
    github = models.URLField(blank=True, default="")
    instagram = models.URLField(blank=True, default="")
    facebook = models.URLField(blank=True, default="")
    twitter = models.URLField(blank=True, default="")
    avatar = models.ImageField(upload_to='profile/', blank=True, null=True)

    class Meta:
        verbose_name = "Profil"

    def __str__(self):
        return self.name_fr


class Skill(models.Model):
    name_fr = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True, default="")
    name_ar = models.CharField(max_length=100, blank=True, default="")
    percentage = models.IntegerField(default=0)
    icon = models.CharField(max_length=50, blank=True, default="")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Compétence"

    def __str__(self):
        return self.name_fr


class Education(models.Model):
    title_fr = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True, default="")
    title_ar = models.CharField(max_length=200, blank=True, default="")
    institution_fr = models.CharField(max_length=200, blank=True, default="")
    institution_en = models.CharField(max_length=200, blank=True, default="")
    institution_ar = models.CharField(max_length=200, blank=True, default="")
    year = models.CharField(max_length=20, blank=True, default="")
    description_fr = models.TextField(blank=True, default="")
    description_en = models.TextField(blank=True, default="")
    description_ar = models.TextField(blank=True, default="")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Formation"

    def __str__(self):
        return self.title_fr


class Experience(models.Model):
    title_fr = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True, default="")
    title_ar = models.CharField(max_length=200, blank=True, default="")
    company_fr = models.CharField(max_length=200, blank=True, default="")
    company_en = models.CharField(max_length=200, blank=True, default="")
    company_ar = models.CharField(max_length=200, blank=True, default="")
    period = models.CharField(max_length=50, blank=True, default="")
    description_fr = models.TextField(blank=True, default="")
    description_en = models.TextField(blank=True, default="")
    description_ar = models.TextField(blank=True, default="")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Expérience"

    def __str__(self):
        return self.title_fr


class Certification(models.Model):
    title_fr = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True, default="")
    title_ar = models.CharField(max_length=200, blank=True, default="")
    issuer = models.CharField(max_length=200, blank=True, default="")
    year = models.CharField(max_length=20, blank=True, default="")
    icon = models.CharField(max_length=50, blank=True, default="")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Certification"

    def __str__(self):
        return self.title_fr


class Article(models.Model):
    CATEGORIES = [
        ('DevOps', 'DevOps'), ('Cloud', 'Cloud'), ('GIS', 'GIS'),
        ('Backend', 'Backend'), ('Linux', 'Linux'), ('AI', 'AI'),
        ('Data', 'Data'), ('Mobile', 'Mobile'), ('Autre', 'Autre'),
    ]

    # ── Identité
    icon          = models.CharField(max_length=50, default="fa-file-code", verbose_name="Icône")
    category      = models.CharField(max_length=100, choices=CATEGORIES, default="DevOps", verbose_name="Catégorie")
    read_time     = models.IntegerField(default=10, verbose_name="Temps de lecture (min)")
    published_date= models.DateField(null=True, blank=True, verbose_name="Date de publication")
    order         = models.IntegerField(default=0, verbose_name="Ordre")
    cover_image   = models.ImageField(upload_to='articles/covers/', blank=True, null=True, verbose_name="Image de couverture")

    # ── Titre (3 langues)
    title_fr = models.CharField(max_length=300, verbose_name="Titre (FR)")
    title_en = models.CharField(max_length=300, blank=True, default="", verbose_name="Titre (EN)")
    title_ar = models.CharField(max_length=300, blank=True, default="", verbose_name="Titre (AR)")

    # ── Sous-titre / chapeau (3 langues)
    subtitle_fr = models.CharField(max_length=500, blank=True, default="", verbose_name="Sous-titre (FR)")
    subtitle_en = models.CharField(max_length=500, blank=True, default="", verbose_name="Sous-titre (EN)")
    subtitle_ar = models.CharField(max_length=500, blank=True, default="", verbose_name="Sous-titre (AR)")

    # ── Résumé carte (3 langues)
    summary_fr = models.TextField(blank=True, default="", verbose_name="Résumé carte (FR)")
    summary_en = models.TextField(blank=True, default="", verbose_name="Résumé carte (EN)")
    summary_ar = models.TextField(blank=True, default="", verbose_name="Résumé carte (AR)")

    # ── Contenu complet CKEditor (3 langues)
    content_fr = CKEditor5Field(blank=True, default="", config_name="article", verbose_name="Contenu complet (FR)")
    content_en = CKEditor5Field(blank=True, default="", config_name="article", verbose_name="Contenu complet (EN)")
    content_ar = CKEditor5Field(blank=True, default="", config_name="article", verbose_name="Contenu complet (AR)")

    class Meta:
        ordering = ['order', '-published_date']
        verbose_name = "Article"

    def __str__(self):
        return self.title_fr or f"Article #{self.pk}"


class CVProtege(models.Model):
    fichier    = models.FileField(upload_to='cv/', verbose_name="Fichier CV (PDF)")
    code       = models.CharField(max_length=50, verbose_name="Code d'accès")
    actif      = models.BooleanField(default=True, verbose_name="Actif")
    nom_fichier= models.CharField(max_length=100, default="CV_Hilla_Prince_Bambe.pdf", verbose_name="Nom téléchargé")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "CV Protégé"

    def __str__(self):
        return f"CV — code: {self.code}"


class ContactMessage(models.Model):
    name       = models.CharField(max_length=100)
    email      = models.EmailField()
    subject    = models.CharField(max_length=200)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read    = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message de contact"

    def __str__(self):
        return f"{self.name} — {self.subject}"
