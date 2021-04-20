from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.user}'

    def last_seen(self):
        return cache.get('last_seen_%s' % self.user)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else:
            return False






