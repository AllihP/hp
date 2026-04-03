import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse


def serve_spa(request):
    """Sert index.html pour toutes les routes React (SPA routing)."""
    index_path = settings.BASE_DIR / 'frontend_dist' / 'index.html'
    try:
        with open(index_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='text/html; charset=utf-8')
    except FileNotFoundError:
        return JsonResponse({'error': 'Frontend not built'}, status=503)


urlpatterns = [
    # Admin Django
    path('admin/',     admin.site.urls),
    # API REST
    path('api/',       include('api.urls')),
    # CKEditor 5
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    # ← TOUT LE RESTE → React SPA (doit être en dernier)
    re_path(r'^.*$',   serve_spa),
]

# Médias uniquement en développement local
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
