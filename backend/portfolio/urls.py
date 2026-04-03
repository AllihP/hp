from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def api_root(request):
    """Point d'entrée API — évite le 'Not Found' sur /"""
    return JsonResponse({
        'status': 'ok',
        'service': 'Portfolio HPB — API',
        'version': '1.0',
        'endpoints': {
            'profile':  '/api/profile/',
            'skills':   '/api/skills/',
            'cv':       '/api/cv/',
            'articles': '/api/articles/',
            'contact':  '/api/contact/',
        }
    })


urlpatterns = [
    path('',        api_root),           # ← évite le 404 sur /
    path('admin/',  admin.site.urls),
    path('api/',    include('api.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

# Servir les médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
