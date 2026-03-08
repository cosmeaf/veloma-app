# authentication/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import SecuritySettings

User = get_user_model()


@receiver(post_save, sender=User)
def create_security_settings(sender, instance, created, **kwargs):

    if created:
        SecuritySettings.objects.create(user=instance)