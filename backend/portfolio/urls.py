import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse


def serve_spa(request):
    """Sert index.html pour toutes les routes React (SPA)."""
    index_path = os.path.join(
        settings.BASE_DIR, 'frontend_dist', 'index.html'
    )
    try:
        with open(index_path, 'rb') as f:
            return HttpResponse(
                f.read(), content_type='text/html; charset=utf-8'
            )
    except FileNotFoundError:
        return JsonResponse({
            'status': 'error',
            'message': 'Frontend non construit.',
            'api': '/api/',
            'admin': '/admin/',
        }, status=503)


urlpatterns = [
    path('sirius/',     admin.site.urls),
    path('api/',       include('api.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),

    # /static/ est géré par WhiteNoise (middleware) — jamais atteint ici
    # Tout le reste → React SPA
    re_path(r'^.*$', serve_spa),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
