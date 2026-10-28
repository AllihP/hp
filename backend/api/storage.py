from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class ArticleImageStorage(FileSystemStorage):
    def __init__(self):
        super().__init__(
            location=os.path.join(settings.MEDIA_ROOT, 'articles', 'images'),
            base_url=settings.MEDIA_URL + 'articles/images/',
        )
