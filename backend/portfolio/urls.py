from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse
import os


def serve_spa(request):
    """
    Sert index.html pour toutes les routes React.
    WhiteNoise gère les fichiers statiques AVANT que cette vue soit appelée,
    donc /assets/index-xxx.js sera servi correctement par WhiteNoise.
    """
    index_path = os.path.join(settings.BASE_DIR, 'frontend_dist', 'index.html')
    try:
        with open(index_path, 'rb') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html; charset=utf-8')
    except FileNotFoundError:
        return JsonResponse({
            'status': 'error',
            'message': 'Frontend non construit. Redéployez le service.',
            'api': '/api/',
            'admin': '/admin/',
        }, status=503)


urlpatterns = [
    # Admin Django
    path('admin/',     admin.site.urls),
    # API REST
    path('api/',       include('api.urls')),
    # CKEditor 5
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    # React SPA — toutes les autres routes
    # WhiteNoise intercepte /assets/* avant cette vue
    re_path(r'^.*$',   serve_spa),
]

# Médias en développement local uniquement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
