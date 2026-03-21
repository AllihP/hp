from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check, name='health'),
    path('profile/', views.get_profile, name='profile'),
    path('skills/', views.get_skills, name='skills'),
    path('cv/', views.get_cv, name='cv'),
    path('articles/', views.get_articles, name='articles'),
    path('contact/', views.send_contact, name='contact'),
]
