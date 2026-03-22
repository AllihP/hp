from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='content_fr',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='article',
            name='content_en',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='article',
            name='content_ar',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='article',
            name='read_time',
            field=models.IntegerField(default=10),
        ),
    ]
