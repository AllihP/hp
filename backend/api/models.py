from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Profile(models.Model):
    name_fr = models.CharField(max_length=100, default="Hilla Prince Bambé")
    name_en = models.CharField(max_length=100, default="Hilla Prince Bambé")
    name_ar = models.CharField(max_length=100, default="هيلا برانس بامبي")
    title_fr = models.CharField(max_length=200, default="Ingénieur des Technologies d'Information")
    title_en = models.CharField(max_length=200, default="Information Technology Engineer")
    title_ar = models.CharField(max_length=200, default="مهندس تكنولوجيا المعلومات")
    bio_fr = models.TextField(default="Jeune ambitieux, je serai un excellent atout pour votre institution notamment dans la gestion de vos projets.")
    bio_en = models.TextField(default="Young and ambitious, I will be a great asset to your institution, particularly in managing your projects.")
    bio_ar = models.TextField(default="شاب طموح، سأكون أصلاً ممتازاً لمؤسستكم، لا سيما في إدارة مشاريعكم.")
    email = models.EmailField(default="hillaprincebambe@gmail.com")
    phone = models.CharField(max_length=30, default="+235 60 92 87 48")
    linkedin = models.URLField(blank=True, default="")
    github = models.URLField(blank=True, default="")
    instagram = models.URLField(blank=True, default="https://www.instagram.com/prince_allih/")
    facebook = models.URLField(blank=True, default="https://www.facebook.com/prince.sirius/")
    twitter = models.URLField(blank=True, default="")

    class Meta:
        verbose_name = "Profil"

    def __str__(self):
        return self.name_fr


class Skill(models.Model):
    name_fr = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    percentage = models.IntegerField(default=50)
    order = models.IntegerField(default=0)
    icon = models.CharField(max_length=50, blank=True, default="")

    class Meta:
        ordering = ['order']
        verbose_name = "Compétence"

    def __str__(self):
        return self.name_fr


class Education(models.Model):
    title_fr = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200)
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
    title_en = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200)
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
    title_en = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200)
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
    title_fr = models.CharField(max_length=300)
    title_en = models.CharField(max_length=300)
    title_ar = models.CharField(max_length=300)
    summary_fr = models.TextField(blank=True, default="")
    summary_en = models.TextField(blank=True, default="")
    summary_ar = models.TextField(blank=True, default="")
    content_fr = CKEditor5Field(blank=True, default="", config_name="article")
    content_en = CKEditor5Field(blank=True, default="", config_name="article")
    content_ar = CKEditor5Field(blank=True, default="", config_name="article")
    read_time = models.IntegerField(default=10)
    icon = models.CharField(max_length=50, default="fa-file-code")
    link = models.URLField(blank=True, default="#")
    published_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=100, blank=True, default="DevOps")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-published_date']
        verbose_name = "Article"

    def __str__(self):
        return self.title_fr


class CVProtege(models.Model):
    """CV protégé par un code secret — un seul enregistrement actif."""
    fichier   = models.FileField(upload_to='cv/', verbose_name="Fichier CV (PDF)")
    code      = models.CharField(max_length=50, verbose_name="Code d'accès secret")
    actif     = models.BooleanField(default=True, verbose_name="Actif")
    nom_fichier = models.CharField(max_length=100, default="CV_Hilla_Prince_Bambe.pdf",
                                   verbose_name="Nom du fichier téléchargé")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "CV Protégé"

    def __str__(self):
        return f"CV — code: {self.code}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message de contact"

    def __str__(self):
        return f"{self.name} - {self.subject}"
