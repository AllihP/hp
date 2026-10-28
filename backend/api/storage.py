from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class ArticleImageStorage(FileSystemStorage):
    def __init__(self):
        super().__init__(
            location=os.path.join(settings.MEDIA_ROOT, 'articles', 'images'),
            base_url=settings.MEDIA_URL + 'articles/images/',
        )


class PrivateFileSystemStorage(FileSystemStorage):
    """Stockage sans URL publique : url() ne renvoie jamais de vrai lien
    (l'admin affiche le nom du fichier avec un lien neutre « # »)."""

    def url(self, name):
        return '#'


def private_storage():
    """
    Stockage HORS de MEDIA_ROOT, sans URL publique.
    Les fichiers (ex. CV protégé) ne sont accessibles que via une vue
    qui vérifie les droits, jamais par un lien direct /media/...
    """
    return PrivateFileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT)
