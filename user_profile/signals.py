from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model

from .models import (
    Person,
    UserProfile
)

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if not created:
        return

    person = Person.objects.create(

        name=instance.username

    )

    UserProfile.objects.create(

        user=instance,

        person=person

    )