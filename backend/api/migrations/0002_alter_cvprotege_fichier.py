"""
Le CV protégé passe dans un stockage privé (PRIVATE_MEDIA_ROOT) pour ne
plus être téléchargeable via /media/cv/... sans le code d'accès.
Les fichiers déjà présents dans media/cv/ sont déplacés vers private/cv/.
"""
import shutil
from pathlib import Path

import api.storage
from django.conf import settings
from django.db import migrations, models


def move_cv_files(apps, schema_editor):
    src = Path(settings.MEDIA_ROOT) / 'cv'
    dst = Path(settings.PRIVATE_MEDIA_ROOT) / 'cv'
    if not src.is_dir():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        if f.is_file() and not (dst / f.name).exists():
            shutil.move(str(f), str(dst / f.name))


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cvprotege',
            name='fichier',
            field=models.FileField(storage=api.storage.private_storage, upload_to='cv/', verbose_name='Fichier CV (PDF)'),
        ),
        migrations.RunPython(move_cv_files, migrations.RunPython.noop),
    ]
