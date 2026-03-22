from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_definitive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='link',
        ),
    ]
