from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Skill, Education, Experience, Certification, Article, ContactMessage

admin.site.site_header = "Portfolio HPB"
admin.site.site_title  = "Portfolio HPB"
admin.site.index_title = "Tableau de bord"


# ── Helpers ────────────────────────────────────────────────────
def field_exists(model, name):
    """Retourne True si le champ existe réellement en base de données."""
    try:
        model._meta.get_field(name)
        return True
    except Exception:
        return False


# ── Profile ────────────────────────────────────────────────────
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name_fr', 'email', 'phone']
    fieldsets = [
        ('Identité',          {'fields': [('name_fr', 'name_en', 'name_ar'), ('title_fr', 'title_en', 'title_ar')]}),
        ('Biographie',        {'fields': ['bio_fr', 'bio_en', 'bio_ar']}),
        ('Contact & Réseaux', {'fields': [('email', 'phone'), ('linkedin', 'github'), ('instagram', 'facebook', 'twitter')]}),
    ]


# ── Skill ──────────────────────────────────────────────────────
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display  = ['name_fr', 'niveau_visuel', 'order']
    list_editable = ['order']
    ordering      = ['order']

    def niveau_visuel(self, obj):
        p = obj.percentage
        c = '#f5c518' if p >= 80 else '#60a5fa' if p >= 50 else '#f87171'
        return format_html(
            '<div style="display:flex;align-items:center;gap:8px">'
            '<div style="width:120px;height:8px;background:#1e2d45;border-radius:4px;overflow:hidden">'
            '<div style="width:{}%;height:100%;background:{};border-radius:4px"></div></div>'
            '<span style="color:{};font-size:11px;font-weight:700">{}%</span></div>',
            p, c, c, p)
    niveau_visuel.short_description = 'Niveau'


# ── Education ──────────────────────────────────────────────────
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display  = ['title_fr', 'institution_fr', 'year', 'order']
    list_editable = ['order']
    ordering      = ['order']
    fieldsets = [
        ('Titre',         {'fields': [('title_fr', 'title_en', 'title_ar')]}),
        ('Établissement', {'fields': [('institution_fr', 'institution_en', 'institution_ar'), 'year']}),
        ('Description',   {'fields': ['description_fr', 'description_en', 'description_ar']}),
        ('Ordre',         {'fields': ['order']}),
    ]


# ── Experience ─────────────────────────────────────────────────
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display  = ['title_fr', 'company_fr', 'period', 'order']
    list_editable = ['order']
    ordering      = ['order']
    fieldsets = [
        ('Poste',       {'fields': [('title_fr', 'title_en', 'title_ar')]}),
        ('Entreprise',  {'fields': [('company_fr', 'company_en', 'company_ar'), 'period']}),
        ('Description', {'fields': ['description_fr', 'description_en', 'description_ar']}),
        ('Ordre',       {'fields': ['order']}),
    ]


# ── Certification ──────────────────────────────────────────────
@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display  = ['title_fr', 'issuer', 'year', 'order']
    list_editable = ['order']
    ordering      = ['order']


# ── Article ────────────────────────────────────────────────────
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    # list_display sans champs optionnels pour éviter les erreurs
    list_display  = ['apercu', 'category', 'order', 'published_date']
    list_editable = ['order']
    list_filter   = ['category']
    ordering      = ['order']
    search_fields = ['title_fr', 'title_en', 'title_ar']

    def apercu(self, obj):
        em = {'fa-github':'🐙','fa-hat-cowboy':'🎩','fa-cloud':'☁️',
              'fa-map':'🗺️','fa-server':'🖥️','fa-robot':'🤖'}
        e = em.get(obj.icon, '📄')
        return format_html(
            '<span style="display:flex;align-items:center;gap:8px">'
            '<span style="font-size:18px">{}</span>'
            '<strong style="color:#fff">{}</strong></span>',
            e, (obj.title_fr or '—')[:65])
    apercu.short_description = 'Article'

    def get_fieldsets(self, request, obj=None):
        """
        Construit les fieldsets dynamiquement selon les champs disponibles.
        Fonctionne AVANT et APRÈS la migration 0002.
        """
        has_content = field_exists(Article, 'content_fr')
        has_readtime = field_exists(Article, 'read_time')

        # Paramètres de base (toujours présents)
        params_fields = ['icon', 'category', 'order']
        if has_readtime:
            params_fields = ['icon', 'category', 'read_time', 'order']

        fieldsets = [
            ('⚙️ Paramètres', {
                'fields': [tuple(params_fields), 'published_date'],
            }),
            ('🇫🇷 Français', {
                'fields': ['title_fr', 'summary_fr'] + (['content_fr'] if has_content else []),
                'classes': ['wide'],
            }),
            ('🇬🇧 English', {
                'fields': ['title_en', 'summary_en'] + (['content_en'] if has_content else []),
                'classes': ['wide', 'collapse'],
            }),
            ('🇸🇦 العربية', {
                'fields': ['title_ar', 'summary_ar'] + (['content_ar'] if has_content else []),
                'classes': ['wide', 'collapse'],
            }),
        ]

        if not has_content:
            fieldsets.append((
                '⚠️ Migration requise',
                {
                    'fields': [],
                    'description': (
                        '<div style="background:rgba(245,197,24,.1);border:1px solid rgba(245,197,24,.3);'
                        'border-radius:8px;padding:14px 18px;color:#f5c518;font-size:13px;">'
                        '⚠️ Les champs de contenu ne sont pas encore disponibles.<br>'
                        'Exécutez : <code style="background:#0a0f1e;padding:2px 8px;border-radius:4px;">'
                        'python manage.py migrate</code> puis redémarrez le serveur.'
                        '</div>'
                    ),
                }
            ))

        return fieldsets

    class Media:
        css = {'all': ['admin/css/hpb_admin.css']}
        js  = ['admin/js/hpb_admin.js']


# ── ContactMessage ─────────────────────────────────────────────
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display    = ['expediteur', 'email', 'subject', 'recu_le', 'statut']
    list_filter     = ['is_read']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    ordering        = ['-created_at']
    actions         = ['marquer_lu']

    def expediteur(self, obj):
        if not obj.is_read:
            return format_html('<span style="color:#f5c518;font-weight:700">● {}</span>', obj.name)
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