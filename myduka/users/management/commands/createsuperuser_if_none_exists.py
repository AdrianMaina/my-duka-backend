# myduka/users/management/commands/createsuperuser_if_none_exists.py

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist.'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

            if not all([username, email, password]):
                self.stdout.write(self.style.ERROR('Superuser environment variables not set. Skipping creation.'))
                return

            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS('Successfully created superuser.'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists. Skipping creation.'))