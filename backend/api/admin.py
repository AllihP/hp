from django.contrib import admin
from .models import Profile, Skill, Education, Experience, Certification, Article, ContactMessage

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name_fr', 'email', 'phone']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name_fr', 'percentage', 'order']
    ordering = ['order']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['title_fr', 'institution_fr', 'year', 'order']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title_fr', 'company_fr', 'period', 'order']

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['title_fr', 'issuer', 'year', 'order']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title_fr', 'category', 'published_date', 'order']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    readonly_fields = ['created_at']
