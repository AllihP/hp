from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_article_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='CVProtege',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fichier', models.FileField(upload_to='cv/', verbose_name='Fichier CV (PDF)')),
                ('code', models.CharField(max_length=50, verbose_name="Code d'accès secret")),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('nom_fichier', models.CharField(default='CV_Hilla_Prince_Bambe.pdf', max_length=100, verbose_name='Nom du fichier téléchargé')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'CV Protégé',
            },
        ),
    ]
