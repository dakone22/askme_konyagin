import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to=os.path.join('avatar', 'uploads'),
                               default=os.path.join('avatar', 'no-image.jpg'), blank=True, null=True)
    biography = models.TextField(max_length=5000)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created: bool, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance: User, **kwargs):
    instance.profile.save()


