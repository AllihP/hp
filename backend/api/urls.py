from django.urls import path
from . import views

urlpatterns = [
    path('',                             views.health_check,         name='health'),
    path('profile/',                     views.get_profile,          name='profile'),
    path('skills/',                      views.get_skills,           name='skills'),
    path('cv/',                          views.get_cv,               name='cv'),
    path('cv/download/',                 views.download_cv,          name='download_cv'),
    path('articles/',                    views.get_articles,         name='articles'),
    path('articles/<uuid:pk>/',          views.get_article_detail,   name='article_detail'),
    path('articles/by_doi/',             views.get_article_by_doi,   name='article_by_doi'),
    path('articles/<uuid:pk>/related/',  views.get_related_articles, name='article_related'),
    path('contact/',                     views.send_contact,         name='contact'),
]
