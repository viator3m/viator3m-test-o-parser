from django.conf import settings as conf
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username=conf.DJANGO_USER).exists():
            User.objects.create_superuser(username=conf.DJANGO_USER,
                                          email=conf.DJANGO_EMAIL,
                                          password=conf.DJANGO_PWD)
