from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Skill, Education, Experience, Certification, Article, CVProtege, ContactMessage

admin.site.site_header = "✍️  Portfolio HPB"
admin.site.site_title  = "Portfolio HPB"
admin.site.index_title = "Tableau de bord"


# ── Profile ────────────────────────────────────────────────────
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name_fr', 'email', 'phone']
    fieldsets = [
        ('Identité',          {'fields': [('name_fr','name_en','name_ar'), ('title_fr','title_en','title_ar')]}),
        ('Biographie',        {'fields': ['bio_fr','bio_en','bio_ar']}),
        ('Contact & Réseaux', {'fields': [('email','phone'),('linkedin','github'),('instagram','facebook','twitter')]}),
        ('Photo',             {'fields': ['avatar']}),
    ]


# ── Skill ──────────────────────────────────────────────────────
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display  = ['name_fr', 'barre', 'order']
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
            p, c, c, p)
    barre.short_description = 'Niveau'


# ── Education ──────────────────────────────────────────────────
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


# ── Experience ─────────────────────────────────────────────────
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


# ── Certification ──────────────────────────────────────────────
@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display  = ['title_fr','issuer','year','order']
    list_editable = ['order']
    ordering      = ['order']


# ── Article ────────────────────────────────────────────────────
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display  = ['apercu', 'categorie_badge', 'duree_badge', 'order', 'published_date']
    list_editable = ['order']
    list_filter   = ['category']
    ordering      = ['order']
    search_fields = ['title_fr','title_en','title_ar']
    save_on_top   = True

    fieldsets = [
        # ── Paramètres généraux
        ('⚙️  Paramètres', {
            'fields': [
                ('icon', 'category'),
                ('read_time', 'order', 'published_date'),
                'cover_image',
            ],
        }),

        # ── Version Française (principale)
        ('🇫🇷  Français — Version principale', {
            'fields': [
                'title_fr',
                'subtitle_fr',
                'summary_fr',
                'content_fr',
            ],
            'classes': ['wide'],
            'description': (
                '<div style="background:rgba(245,197,24,.08);border-left:3px solid #f5c518;'
                'padding:10px 14px;border-radius:0 6px 6px 0;font-size:12px;color:#94a3b8;margin-bottom:8px">'
                '<strong style="color:#f5c518">Guide de rédaction :</strong> '
                'Utilisez <strong>H1</strong> pour les grandes parties, '
                '<strong>H2 ★</strong> pour les sections numérotées (apparaissent dans le sommaire), '
                '<strong>H3</strong> pour les sous-sections. '
                'Insérez des images directement avec le bouton 📷. '
                'Le <strong>Ctrl+S</strong> sauvegarde.'
                '</div>'
            ),
        }),

        # ── Version Anglaise
        ('🇬🇧  English — Optional', {
            'fields': ['title_en', 'subtitle_en', 'summary_en', 'content_en'],
            'classes': ['wide', 'collapse'],
        }),

        # ── Version Arabe
        ('🇸🇦  العربية — اختياري', {
            'fields': ['title_ar', 'subtitle_ar', 'summary_ar', 'content_ar'],
            'classes': ['wide', 'collapse'],
        }),
    ]

    def apercu(self, obj):
        em = {'fa-github':'🐙','fa-hat-cowboy':'🎩','fa-cloud':'☁️',
              'fa-map':'🗺️','fa-server':'🖥️','fa-robot':'🤖','fa-file-code':'📄'}
        e = em.get(obj.icon, '📄')
        img_html = ''
        if obj.cover_image:
            img_html = format_html(
                '<img src="{}" style="width:36px;height:36px;border-radius:4px;object-fit:cover;margin-right:8px;vertical-align:middle">',
                obj.cover_image.url
            )
        return format_html(
            '<span style="display:flex;align-items:center;gap:8px">'
            '{}<span style="font-size:16px">{}</span>'
            '<strong style="color:#fff">{}</strong></span>',
            img_html, e, (obj.title_fr or '—')[:60])
    apercu.short_description = 'Article'

    def categorie_badge(self, obj):
        colors = {
            'DevOps':'#f5c518','Cloud':'#60a5fa','GIS':'#34d399',
            'Backend':'#a5b4fc','Linux':'#f87171','AI':'#fb923c',
            'Data':'#e879f9','Mobile':'#38bdf8','Autre':'#94a3b8',
        }
        c = colors.get(obj.category, '#94a3b8')
        return format_html(
            '<span style="background:{1}22;border:1px solid {1}55;color:{1};'
            'padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700">{0}</span>',
            obj.category, c)
    categorie_badge.short_description = 'Catégorie'

    def duree_badge(self, obj):
        return format_html(
            '<span style="background:rgba(96,165,250,.12);border:1px solid rgba(96,165,250,.3);'
            'color:#60a5fa;padding:3px 9px;border-radius:12px;font-size:11px">⏱ {} min</span>',
            obj.read_time or 10)
    duree_badge.short_description = 'Durée'

    class Media:
        css = {'all': ['admin/css/hpb_admin.css']}
        js  = ['admin/js/hpb_admin.js']


# ── CV Protégé ─────────────────────────────────────────────────
@admin.register(CVProtege)
class CVProtegeAdmin(admin.ModelAdmin):
    list_display  = ['nom_fichier', 'code_masque', 'actif', 'updated_at']
    list_editable = ['actif']
    fieldsets = [
        ('Fichier CV',   {'fields': ['fichier','nom_fichier']}),
        ('Protection',   {'fields': ['code','actif'],
                          'description': 'Transmettez ce code au recruteur par email/WhatsApp.'}),
    ]

    def code_masque(self, obj):
        c = obj.code or ''
        m = c[:2] + '●' * max(0, len(c)-2)
        return format_html(
            '<code style="color:#f5c518;letter-spacing:.06em;background:rgba(245,197,24,.1);'
            'padding:2px 8px;border-radius:4px">{}</code>', m)
    code_masque.short_description = 'Code (masqué)'


# ── Messages de contact ────────────────────────────────────────
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
        if obj.is_read:
            return format_html('<span style="color:#34d399;font-size:11px">✓ Lu</span>')
        return format_html('<span style="color:#f5c518;font-size:11px;font-weight:700">● Non lu</span>')
    statut.short_description = 'Statut'

    def marquer_lu(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} message(s) marqué(s) comme lu(s).')
    marquer_lu.short_description = '✔ Marquer comme lu'

    def has_add_permission(self, request):
        return False
