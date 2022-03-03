from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def handle_new_job(sender, **kwargs):
    if kwargs.get('created', False):
        user = kwargs.get('instance')
        g = Group.objects.get(name='Students')
        user.groups.add(g)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.generate_key()
