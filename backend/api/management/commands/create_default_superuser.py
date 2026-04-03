"""
management/commands/create_default_superuser.py

Crée automatiquement un superuser depuis les variables d'environnement.
Appelé pendant le build Render — pas besoin du Shell (payant).

Variables requises sur Render → Environment :
    DJANGO_SUPERUSER_USERNAME  (ex: hillaprince)
    DJANGO_SUPERUSER_EMAIL     (ex: hillaprincebambe@gmail.com)
    DJANGO_SUPERUSER_PASSWORD  (ex: MonMotDePasse2026!)
"""

import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crée un superuser depuis les variables d'environnement (déploiement Render)"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                '⚠️  DJANGO_SUPERUSER_USERNAME ou DJANGO_SUPERUSER_PASSWORD '
                'non définis — superuser non créé.'
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(
                f'ℹ️  Superuser "{username}" existe déjà — rien à faire.'
            ))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(
            f'✅ Superuser "{username}" créé avec succès !'
        ))
