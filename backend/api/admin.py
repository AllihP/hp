import json
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (Profile, Skill, Education, Experience, Certification,
                     Author, Article, ArticleAuthor, ArticleAttachment,
                     CVProtege, ContactMessage)

admin.site.site_header = "✍️  Portfolio HPB"
admin.site.site_title  = "Portfolio HPB"
admin.site.index_title = "Tableau de bord"


# ══ Widget image stylé ════════════════════════════════════════════
class StyledImageWidget(forms.ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        has_image = bool(value and hasattr(value, 'url'))
        preview   = ''
        if has_image:
            preview = (
                f'<div style="margin-bottom:12px;border-radius:10px;overflow:hidden;'
                f'border:1px solid rgba(245,197,24,.25);display:inline-block;'
                f'background:#0d1525;position:relative">'
                f'<img src="{value.url}" style="display:block;max-width:380px;'
                f'max-height:200px;object-fit:cover;border-radius:10px">'
                f'<div style="position:absolute;top:8px;right:8px;background:rgba(8,15,30,.8);'
                f'border:1px solid rgba(245,197,24,.35);border-radius:6px;padding:3px 10px;'
                f'font-size:11px;color:#f5c518;font-weight:600">✓ Image actuelle</div></div>'
            )

        input_html = super().render(name, value, attrs={
            **(attrs or {}),
            'id': f'id_{name}',
            'accept': 'image/*',
            'style': 'display:none',
            'onchange': f'hpbPreview(this,"{name}")',
        }, renderer=renderer)

        return mark_safe(f"""
        {preview}
        <div onclick="document.getElementById('id_{name}').click()" style="
          border:2px dashed rgba(245,197,24,.3);border-radius:10px;padding:22px 18px;
          text-align:center;cursor:pointer;background:rgba(245,197,24,.04);
          transition:all .25s;max-width:400px;"
          onmouseover="this.style.borderColor='rgba(245,197,24,.7)';this.style.background='rgba(245,197,24,.08)'"
          onmouseout="this.style.borderColor='rgba(245,197,24,.3)';this.style.background='rgba(245,197,24,.04)'"
          ondragover="event.preventDefault();this.style.borderColor='#f5c518'"
          ondrop="hpbDrop(event,'id_{name}','{name}')">
          <div style="font-size:2rem;margin-bottom:8px">🖼️</div>
          <div style="font-size:13px;color:#f5c518;font-weight:600;margin-bottom:4px">
            Cliquer ou glisser-déposer une image
          </div>
          <div style="font-size:11px;color:rgba(255,255,255,.35)">
            JPG, PNG, WEBP — Max 10 MB
          </div>
        </div>
        <div id="new-preview-{name}" style="margin-top:10px;display:none">
          <img id="new-img-{name}" style="max-width:380px;max-height:200px;
            object-fit:cover;border-radius:10px;border:1px solid rgba(245,197,24,.3);display:block">
          <p style="font-size:11px;color:#34d399;margin-top:5px">✓ Nouvelle image sélectionnée</p>
        </div>
        {input_html}
        <script>
        function hpbPreview(input,name){{
          var f=input.files[0];if(!f)return;
          var r=new FileReader();r.onload=function(e){{
            var p=document.getElementById('new-preview-'+name);
            var i=document.getElementById('new-img-'+name);
            i.src=e.target.result;p.style.display='block';
          }};r.readAsDataURL(f);
        }}
        function hpbDrop(e,inputId,name){{
          e.preventDefault();var dt=e.dataTransfer;
          if(dt.files.length){{
            var inp=document.getElementById(inputId);
            var t=new DataTransfer();t.items.add(dt.files[0]);
            inp.files=t.files;hpbPreview(inp,name);
          }}
        }}
        </script>
        """)


# ══ Profile ═══════════════════════════════════════════════════════
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name_fr', 'email', 'phone']
    fieldsets = [
        ('Identité',          {'fields': [('name_fr','name_en','name_ar'),('title_fr','title_en','title_ar')]}),
        ('Biographie',        {'fields': ['bio_fr','bio_en','bio_ar']}),
        ('Contact & Réseaux', {'fields': [('email','phone'),('linkedin','github'),('instagram','facebook','twitter')]}),
        ('Photo',             {'fields': ['avatar']}),
    ]


# ══ Compétences, Formations, Expériences, Certifications ══════════
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display  = ['name_fr','barre','order']
    list_editable = ['order']
    ordering      = ['order']

    def barre(self, obj):
        p = obj.percentage
        c = '#f5c518' if p >= 80 else '#60a5fa' if p >= 50 else '#f87171'
        return format_html(
            '<div style="display:flex;align-items:center;gap:8px">'
            '<div style="width:120px;height:8px;background:#1e2d45;border-radius:4px;overflow:hidden">'
            '<div style="width:{}%;height:100%;background:{};border-radius:4px"></div></div>'
            '<span style="color:{};font-size:11px;font-weight:700">{}%</span></div>',
            p,c,c,p)
    barre.short_description = 'Niveau'


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display  = ['title_fr','institution_fr','year','order']
    list_editable = ['order']
    ordering      = ['order']
    fieldsets = [
        ('Titre',         {'fields': [('title_fr','title_en','title_ar')]}),
        ('Établissement', {'fields': [('institution_fr','institution_en','institution_ar'),'year']}),
        ('Description',   {'fields': ['description_fr','description_en','description_ar']}),
        ('Ordre',         {'fields': ['order']}),
    ]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display  = ['title_fr','company_fr','period','order']
    list_editable = ['order']
    ordering      = ['order']
    fieldsets = [
        ('Poste',       {'fields': [('title_fr','title_en','title_ar')]}),
        ('Entreprise',  {'fields': [('company_fr','company_en','company_ar'),'period']}),
        ('Description', {'fields': ['description_fr','description_en','description_ar']}),
        ('Ordre',       {'fields': ['order']}),
    ]


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display  = ['title_fr','issuer','year','order']
    list_editable = ['order']
    ordering      = ['order']


# ══ AUTEURS ═══════════════════════════════════════════════════════
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display  = ['fiche','affiliation','orcid_link','is_corresponding']
    list_filter   = ['is_corresponding','country']
    search_fields = ['first_name','last_name','affiliation','email']
    fieldsets = [
        ('Identité', {
            'fields': ['title',('first_name','last_name'),'photo'],
        }),
        ('Institution', {
            'fields': ['affiliation','country','email','orcid'],
        }),
        ('Biographie', {
            'fields': ['bio_fr','bio_en'],
            'classes': ['collapse'],
        }),
        ('Statut', {
            'fields': ['is_corresponding'],
        }),
    ]

    def fiche(self, obj):
        av = ''
        if obj.photo:
            try:
                av = format_html(
                    '<img src="{}" style="width:32px;height:32px;border-radius:50%;'
                    'object-fit:cover;margin-right:8px;vertical-align:middle">',
                    obj.photo.url)
            except Exception:
                pass
        title = f"{obj.title} " if obj.title else ""
        return format_html('{}<strong style="color:#fff">{}{} {}</strong>',
                           av, title, obj.first_name, obj.last_name)
    fiche.short_description = 'Auteur'

    def orcid_link(self, obj):
        if obj.orcid:
            return format_html(
                '<a href="https://orcid.org/{0}" target="_blank" '
                'style="color:#a3e635;font-family:monospace;font-size:11px">{0}</a>',
                obj.orcid)
        return mark_safe('<span style="color:rgba(255,255,255,.25)">—</span>')
    orcid_link.short_description = 'ORCID'


# ══ ARTICLES — Inlines ════════════════════════════════════════════
class ArticleAuthorInline(admin.TabularInline):
    model   = ArticleAuthor
    extra   = 1
    ordering = ['order']
    fields  = ['order','author']
    verbose_name = "Auteur"
    verbose_name_plural = "Auteurs (ordre d'affichage)"


class ArticleAttachmentInline(admin.TabularInline):
    model   = ArticleAttachment
    extra   = 0
    fields  = ['file','file_type','description_fr','description_en']
    verbose_name = "Pièce jointe"


# ══ Formulaire Article avec widgets personnalisés ═════════════════
class ArticleAdminForm(forms.ModelForm):

    def _clean_json_field(self, field_name, default):
        value = self.cleaned_data.get(field_name)
        if value is None or value == '' or value == 'null':
            return default
        if isinstance(value, (list, dict)):
            return value
        import json
        try:
            parsed = json.loads(value)
            return parsed
        except (json.JSONDecodeError, TypeError):
            return default

    def clean_key_metrics(self):
        return self._clean_json_field('key_metrics', [])

    def clean_content_sections(self):
        return self._clean_json_field('content_sections', [])

    def clean_references(self):
        return self._clean_json_field('references', [])

    class Meta:
        model   = Article
        fields  = '__all__'
        widgets = {
            'og_image': StyledImageWidget(),
            'key_metrics': forms.Textarea(attrs={
                'rows': 6,
                'style': 'font-family:monospace;font-size:12px;background:#090f1c;color:#a5f3fc;border:1px solid rgba(245,197,24,.25);border-radius:8px;padding:10px',
                'placeholder': '[{"label":"Réseau cartographié","value":"1 015","unit":"km","icon":"🛣️"},{"label":"PCI moyen","value":"46.0","unit":"","icon":"📊"}]'
            }),
            'content_sections': forms.Textarea(attrs={
                'rows': 20,
                'style': 'font-family:monospace;font-size:12px;background:#090f1c;color:#a5f3fc;border:1px solid rgba(245,197,24,.25);border-radius:8px;padding:10px',
                'placeholder': '[{"order":1,"slug":"introduction","title_fr":"Introduction","title_en":"Introduction","title_ar":"مقدمة","content_fr":"<p>Votre texte...</p>","content_en":"","content_ar":""}]'
            }),
            'references': forms.Textarea(attrs={
                'rows': 8,
                'style': 'font-family:monospace;font-size:12px;background:#090f1c;color:#a5f3fc;border:1px solid rgba(245,197,24,.25);border-radius:8px;padding:10px',
                'placeholder': '["ASTM (2020). D6433-20...", "Banque mondiale (2023). Chad Report..."]'
            }),
        }


# ══ ARTICLE ADMIN ═════════════════════════════════════════════════
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form          = ArticleAdminForm
    inlines       = [ArticleAuthorInline, ArticleAttachmentInline]
    list_display  = ['apercu','statut_badge','journal_name','annee','vues']
    list_filter   = ['status','year']
    search_fields = ['title_fr','title_en','doi']
    save_on_top   = True
    date_hierarchy = 'published_at'

    fieldsets = [

        # ── Image de couverture ───────────────────────────────
        ('🖼️  Image de couverture', {
            'fields': ['og_image'],
            'description': (
                '<p style="color:#94a3b8;font-size:12px;margin:6px 0 12px">'
                'S\'affiche en miniature stylée à côté du titre et en couverture plein écran.</p>'
            ),
        }),

        # ── Paramètres ────────────────────────────────────────
        ('⚙️  Paramètres', {
            'fields': [
                ('doi', 'status'),
                ('journal_name', 'volume', 'year'),
                'published_at',
            ],
        }),

        # ── Titres + sous-titres ──────────────────────────────
        ('🇫🇷  Titre & sous-titre (FR)', {
            'fields': ['title_fr', 'subtitle_fr'],
        }),
        ('🇬🇧  Title & subtitle (EN)', {
            'fields': ['title_en', 'subtitle_en'],
            'classes': ['collapse'],
        }),
        ('🇸🇦  العنوان والعنوان الفرعي (AR)', {
            'fields': ['title_ar', 'subtitle_ar'],
            'classes': ['collapse'],
        }),

        # ── Résumés ───────────────────────────────────────────
        ('📝  Résumés', {
            'fields': ['abstract_fr', 'abstract_en', 'abstract_ar'],
        }),

        # ── Mots-clés ─────────────────────────────────────────
        ('🏷️  Mots-clés', {
            'fields': [('keywords_fr', 'keywords_en', 'keywords_ar')],
            'description': '<p style="color:#94a3b8;font-size:12px">Séparés par des virgules.</p>',
        }),

        # ── Statistiques clés ─────────────────────────────────
        ('📊  Statistiques clés', {
            'fields': ['key_metrics'],
            'description': (
                '<div style="background:rgba(245,197,24,.07);border-left:3px solid #f5c518;'
                'padding:10px 14px;border-radius:0 6px 6px 0;font-size:12px;color:#94a3b8;margin-bottom:8px">'
                '<strong style="color:#f5c518">Exemple :</strong><br>'
                '<code style="color:#60a5fa;font-size:11px">'
                '[{"label":"Réseau cartographié","value":"1 015","unit":"km","icon":"🛣️"},'
                '{"label":"PCI moyen","value":"46.0","unit":"","icon":"📊"},'
                '{"label":"Précision IA","value":"91,3","unit":"%","icon":"🤖"}]'
                '</code></div>'
            ),
        }),

        # ── Sections de contenu ───────────────────────────────
        ('✍️  Contenu de l\'article (sections JSON)', {
            'fields': ['content_sections'],
            'description': (
                '<div style="background:rgba(96,165,250,.07);border-left:3px solid #60a5fa;'
                'padding:10px 14px;border-radius:0 6px 6px 0;font-size:12px;color:#94a3b8;margin-bottom:8px">'
                '<strong style="color:#60a5fa">Structure d\'une section :</strong><br>'
                '<code style="color:#a5f3fc;font-size:11px">'
                '{"order":1, "slug":"introduction", '
                '"title_fr":"1. Introduction", "title_en":"Introduction", "title_ar":"مقدمة", '
                '"content_fr":"&lt;p&gt;Texte HTML...&lt;/p&gt;", '
                '"content_en":"", "content_ar":""}'
                '</code><br><br>'
                '<strong style="color:#60a5fa">Conseil :</strong> '
                'Rédigez le HTML dans CKEditor d\'un brouillon, puis copiez-collez ici.'
                '</div>'
            ),
        }),

        # ── Références ────────────────────────────────────────
        ('📚  Références bibliographiques', {
            'fields': ['references'],
            'classes': ['collapse'],
            'description': (
                '<p style="color:#94a3b8;font-size:12px">'
                'Tableau JSON de chaînes. Ex: ["Auteur (2020). Titre. Revue.", "..."]</p>'
            ),
        }),

        # ── SEO ───────────────────────────────────────────────
        ('🔍  SEO (optionnel)', {
            'fields': ['meta_description_fr', 'meta_description_en', 'meta_description_ar'],
            'classes': ['collapse'],
        }),
    ]

    # ── Méthodes d'affichage liste ────────────────────────────
    def apercu(self, obj):
        img = ''
        if obj.og_image:
            try:
                img = format_html(
                    '<img src="{}" style="width:44px;height:44px;border-radius:6px;'
                    'object-fit:cover;margin-right:10px;vertical-align:middle;'
                    'border:1px solid rgba(245,197,24,.35)">',
                    obj.og_image.url)
            except Exception:
                pass
        return format_html(
            '<span style="display:flex;align-items:center">'
            '{}<strong style="color:#fff">{}</strong></span>',
            img, (obj.title_fr or '—')[:60])
    apercu.short_description = 'Article'

    def statut_badge(self, obj):
        colors = {
            'draft': '#94a3b8', 'review': '#fb923c',
            'published': '#34d399', 'archived': '#f87171',
        }
        labels = {
            'draft': 'Brouillon', 'review': 'En révision',
            'published': 'Publié', 'archived': 'Archivé',
        }
        c = colors.get(obj.status, '#94a3b8')
        return format_html(
            '<span style="background:{0}22;border:1px solid {0}55;color:{0};'
            'padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600">{1}</span>',
            c, labels.get(obj.status, obj.status))
    statut_badge.short_description = 'Statut'

    def annee(self, obj):
        return format_html('<span style="color:rgba(255,255,255,.55)">{}</span>', obj.year)
    annee.short_description = 'Année'

    def vues(self, obj):
        return format_html('<span style="color:#60a5fa;font-size:11px">👁 {}</span>', obj.view_count)
    vues.short_description = 'Vues'

    class Media:
        css = {'all': ['admin/css/hpb_admin.css']}
        js  = ['admin/js/hpb_admin.js']


# ══ CV PROTÉGÉ ════════════════════════════════════════════════════
@admin.register(CVProtege)
class CVProtegeAdmin(admin.ModelAdmin):
    list_display  = ['nom_fichier','code_masque','actif','updated_at']
    list_editable = ['actif']
    fieldsets = [
        ('Fichier CV',  {'fields': ['fichier','nom_fichier']}),
        ('Protection',  {'fields': ['code','actif']}),
    ]

    def code_masque(self, obj):
        c = obj.code or ''
        m = c[:2] + '●' * max(0, len(c)-2)
        return format_html(
            '<code style="color:#f5c518;letter-spacing:.06em;background:rgba(245,197,24,.1);'
            'padding:2px 8px;border-radius:4px">{}</code>', m)
    code_masque.short_description = 'Code (masqué)'


# ══ MESSAGES CONTACT ══════════════════════════════════════════════
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display    = ['expediteur','email','subject','recu_le','statut']
    list_filter     = ['is_read']
    readonly_fields = ['name','email','subject','message','created_at']
    ordering        = ['-created_at']
    actions         = ['marquer_lu']

    def expediteur(self, obj):
        if not obj.is_read:
            return format_html('<strong style="color:#f5c518">● {}</strong>', obj.name)
        return obj.name
    expediteur.short_description = 'Expéditeur'

    def recu_le(self, obj):
        return obj.created_at.strftime('%d/%m/%Y %H:%M')
    recu_le.short_description = 'Reçu le'

    def statut(self, obj):
        try:
            lu = obj.is_read
        except Exception:
            lu = False
        if lu:
            return mark_safe('<span style="color:#34d399;font-size:11px">✓ Lu</span>')
        return mark_safe('<span style="color:#f5c518;font-size:11px;font-weight:700">● Non lu</span>')
    statut.short_description = 'Statut'

    def marquer_lu(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} message(s) marqué(s) comme lu(s).')
    marquer_lu.short_description = '✔ Marquer comme lu'

    def has_add_permission(self, request):
        return False
