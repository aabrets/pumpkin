import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from annoying.fields import AutoOneToOneField


@python_2_unicode_compatible
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserProfile(models.Model):
    user = AutoOneToOneField(User, on_delete='PROTECT')
    follows = models.ManyToManyField('UserProfile', related_name='followed_by')
    favorites = models.ManyToManyField('recipes.Recipe', related_name='favorited_by')

    def __unicode__(self):
        return self.user.username
