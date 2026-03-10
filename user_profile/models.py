from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Person(models.Model):

    name = models.CharField(max_length=255)

    nif = models.CharField(max_length=50, blank=True)

    phone = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.name


class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE
    )

    onboarding_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"profile:{self.user_id}"