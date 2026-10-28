"""
IP réelle du visiteur derrière le proxy de Render.

Le client peut écrire ce qu'il veut dans X-Forwarded-For ; seules les
dernières entrées (ajoutées par nos proxys de confiance) sont fiables.
Même logique que REST_FRAMEWORK['NUM_PROXIES'] côté DRF.
"""
from django.conf import settings


def get_client_ip(request):
    num_proxies = settings.REST_FRAMEWORK.get('NUM_PROXIES') or 0
    remote_addr = request.META.get('REMOTE_ADDR')
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff and num_proxies > 0:
        addrs = [a.strip() for a in xff.split(',') if a.strip()]
        if addrs:
            return addrs[-min(num_proxies, len(addrs))]
    return remote_addr
