from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
import uuid


# ══════════════════════════════════════════════════════════════════
#  MODÈLES EXISTANTS (inchangés)
# ══════════════════════════════════════════════════════════════════

class Profile(models.Model):
    name_fr = models.CharField(max_length=100, default="Hilla Prince Bambé")
    name_en = models.CharField(max_length=100, default="Hilla Prince Bambé")
    name_ar = models.CharField(max_length=100, default="هيلا برانس بامبي")
    title_fr = models.CharField(max_length=200, default="Chargé de Projet")
    title_en = models.CharField(max_length=200, default="Project Manager")
    title_ar = models.CharField(max_length=200, default="مدير مشروع")
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


# ══════════════════════════════════════════════════════════════════
#  NOUVEAU SYSTÈME D'ARTICLES SCIENTIFIQUES
# ══════════════════════════════════════════════════════════════════

class Author(models.Model):
    """Auteur d'article — peut être lié à plusieurs articles."""
    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name     = models.CharField(max_length=100, verbose_name="Prénom")
    last_name      = models.CharField(max_length=100, verbose_name="Nom")
    title          = models.CharField(max_length=50, blank=True,
                                      verbose_name="Titre (Dr, Pr, Ing…)")
    affiliation    = models.CharField(max_length=300, blank=True,
                                      verbose_name="Affiliation / Institution")
    email          = models.EmailField(blank=True)
    orcid          = models.CharField(max_length=50, blank=True,
                                      verbose_name="ORCID iD",
                                      help_text="Ex: 0000-0001-2345-6789")
    country        = models.CharField(max_length=100, blank=True, verbose_name="Pays")
    is_corresponding = models.BooleanField(default=False,
                                           verbose_name="Auteur correspondant")
    photo          = models.ImageField(upload_to='authors/', blank=True, null=True,
                                       verbose_name="Photo")
    bio_fr         = models.TextField(blank=True, verbose_name="Biographie (FR)")
    bio_en         = models.TextField(blank=True, verbose_name="Biography (EN)")

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Auteur"

    def __str__(self):
        parts = [p for p in [self.title, self.first_name, self.last_name] if p]
        return " ".join(parts)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Article(models.Model):
    """Article scientifique complet avec contenu structuré multilingue."""

    STATUS_CHOICES = [
        ('draft',     'Brouillon'),
        ('review',    'En révision'),
        ('published', 'Publié'),
        ('archived',  'Archivé'),
    ]

    # ── Identité ──────────────────────────────────────────────
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doi         = models.CharField(max_length=150, unique=True, blank=True,
                                   verbose_name="DOI",
                                   help_text="Ex: 10.xxxx/rgiu.2026.001")
    journal_name = models.CharField(max_length=200,
                                    default="Portfolio HPB · Articles",
                                    verbose_name="Nom de la revue")
    volume      = models.CharField(max_length=50, blank=True, default="Vol. 1",
                                   verbose_name="Volume / numéro")
    year        = models.IntegerField(default=2026, verbose_name="Année")
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES,
                                   default='draft', verbose_name="Statut")

    # ── Image de couverture / OG ──────────────────────────────
    og_image    = models.ImageField(upload_to='articles/covers/', blank=True, null=True,
                                    verbose_name="Image de couverture (OG)")

    # ── Titres multilingues ───────────────────────────────────
    title_fr    = models.CharField(max_length=500, verbose_name="Titre (FR)")
    title_en    = models.CharField(max_length=500, blank=True, default="",
                                   verbose_name="Titre (EN)")
    title_ar    = models.CharField(max_length=500, blank=True, default="",
                                   verbose_name="Titre (AR)")

    # ── Sous-titres multilingues ──────────────────────────────
    subtitle_fr = models.CharField(max_length=500, blank=True, default="",
                                   verbose_name="Sous-titre (FR)")
    subtitle_en = models.CharField(max_length=500, blank=True, default="",
                                   verbose_name="Sous-titre (EN)")
    subtitle_ar = models.CharField(max_length=500, blank=True, default="",
                                   verbose_name="Sous-titre (AR)")

    # ── Résumés multilingues ──────────────────────────────────
    abstract_fr = models.TextField(verbose_name="Résumé (FR)")
    abstract_en = models.TextField(blank=True, default="", verbose_name="Abstract (EN)")
    abstract_ar = models.TextField(blank=True, default="", verbose_name="الملخص (AR)")

    # ── Mots-clés (virgule-séparés par langue) ────────────────
    keywords_fr = models.CharField(max_length=500, blank=True, default="",
                                   verbose_name="Mots-clés FR (virgules)")
    keywords_en = models.CharField(max_length=500, blank=True, default="",
                                   verbose_name="Keywords EN (commas)")
    keywords_ar = models.CharField(max_length=500, blank=True, default="",
                                   verbose_name="كلمات مفتاحية (فواصل)")

    # ── Statistiques clés (JSON) ──────────────────────────────
    key_metrics = models.JSONField(
        default=list, blank=True,
        verbose_name="Statistiques clés (JSON)",
        help_text=(
            'Ex: [{"label":"Réseau cartographié","value":"1 015","unit":"km","icon":"🛣️"},'
            '{"label":"PCI moyen","value":"46.0","unit":"","icon":"📊"}]'
        )
    )

    # ── Contenu par sections (JSON + CKEditor) ────────────────
    content_sections = models.JSONField(
        default=list, blank=True,
        verbose_name="Sections de l'article (JSON)",
        help_text=(
            'Structure: [{"order":1,"slug":"introduction",'
            '"title_fr":"Introduction","title_en":"Introduction","title_ar":"مقدمة",'
            '"content_fr":"<p>...</p>","content_en":"","content_ar":""}]'
        )
    )

    # ── Références bibliographiques (JSON) ────────────────────
    references = models.JSONField(
        default=list, blank=True,
        verbose_name="Références bibliographiques (JSON)",
        help_text='Ex: ["ASTM (2020). D6433-20...","Banque mondiale (2023)..."]'
    )

    # ── Auteurs ───────────────────────────────────────────────
    authors = models.ManyToManyField(
        'Author',
        through='ArticleAuthor',
        related_name='articles',
        blank=True,
    )

    # ── SEO ───────────────────────────────────────────────────
    meta_description_fr = models.TextField(blank=True, default="")
    meta_description_en = models.TextField(blank=True, default="")
    meta_description_ar = models.TextField(blank=True, default="")

    # ── Dates & stats ─────────────────────────────────────────
    submitted_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True,
                                        verbose_name="Date de publication")
    updated_at   = models.DateTimeField(auto_now=True)
    view_count   = models.IntegerField(default=0)

    class Meta:
        ordering  = ['-published_at', '-submitted_at']
        verbose_name = "Article"

    def __str__(self):
        return f"{self.doi or str(self.id)[:8]} · {self.title_fr[:60]}"

    def save(self, *args, **kwargs):
        if not self.doi:
            self.doi = f"10.kiceko/hpb.{self.year}.{str(self.id)[:8]}"
        super().save(*args, **kwargs)


class ArticleAuthor(models.Model):
    """Liaison ordonnée Article ↔ Auteur."""
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author  = models.ForeignKey(Author, on_delete=models.CASCADE)
    order   = models.IntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        ordering = ['order']
        unique_together = ['article', 'author']
        verbose_name = "Auteur d'article"

    def __str__(self):
        return f"{self.article} · {self.author}"


class ArticleAttachment(models.Model):
    """Fichiers joints à un article (PDF, données, etc.)."""
    TYPE_CHOICES = [
        ('pdf',           'PDF'),
        ('data',          'Données'),
        ('supplementary', 'Matériel supplémentaire'),
        ('code',          'Code source'),
    ]
    article       = models.ForeignKey(Article, on_delete=models.CASCADE,
                                      related_name='attachments')
    file          = models.FileField(upload_to='articles/attachments/')
    file_type     = models.CharField(max_length=50, choices=TYPE_CHOICES, default='pdf')
    description_fr = models.CharField(max_length=300, blank=True)
    description_en = models.CharField(max_length=300, blank=True)
    uploaded_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pièce jointe"

    def __str__(self):
        return f"{self.article} — {self.file_type}"
