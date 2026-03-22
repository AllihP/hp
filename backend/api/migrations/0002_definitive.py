"""
Migration 0002 — définitive
Ajoute tous les champs Article (content, subtitle, cover_image)
+ CVProtege
Remplace toutes les migrations conflictuelles précédentes.
"""
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        # ── Article : nouveaux champs ─────────────────────────
        migrations.AddField(
            model_name='article',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='articles/covers/', verbose_name='Image de couverture'),
        ),
        migrations.AddField(
            model_name='article',
            name='read_time',
            field=models.IntegerField(default=10, verbose_name='Temps de lecture (min)'),
        ),
        migrations.AddField(
            model_name='article',
            name='subtitle_fr',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Sous-titre (FR)'),
        ),
        migrations.AddField(
            model_name='article',
            name='subtitle_en',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Sous-titre (EN)'),
        ),
        migrations.AddField(
            model_name='article',
            name='subtitle_ar',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Sous-titre (AR)'),
        ),
        migrations.AddField(
            model_name='article',
            name='content_fr',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, config_name='article', default='', verbose_name='Contenu complet (FR)'),
        ),
        migrations.AddField(
            model_name='article',
            name='content_en',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, config_name='article', default='', verbose_name='Contenu complet (EN)'),
        ),
        migrations.AddField(
            model_name='article',
            name='content_ar',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, config_name='article', default='', verbose_name='Contenu complet (AR)'),
        ),
        # Mettre à jour choices category
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(
                choices=[
                    ('DevOps','DevOps'),('Cloud','Cloud'),('GIS','GIS'),
                    ('Backend','Backend'),('Linux','Linux'),('AI','AI'),
                    ('Data','Data'),('Mobile','Mobile'),('Autre','Autre'),
                ],
                default='DevOps', max_length=100, verbose_name='Catégorie'
            ),
        ),
        # ── CVProtege ─────────────────────────────────────────
        migrations.CreateModel(
            name='CVProtege',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fichier', models.FileField(upload_to='cv/', verbose_name='Fichier CV (PDF)')),
                ('code', models.CharField(max_length=50, verbose_name="Code d'accès")),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('nom_fichier', models.CharField(default='CV_Hilla_Prince_Bambe.pdf', max_length=100, verbose_name='Nom téléchargé')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'verbose_name': 'CV Protégé'},
        ),
    ]
