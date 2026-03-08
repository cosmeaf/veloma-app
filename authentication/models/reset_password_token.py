# authentication/models/reset_password_token.py

import uuid
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone


class ResetPasswordToken(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens",
    )

    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["user"])]

    def is_valid(self):
        return (timezone.now() - self.created_at) <= timedelta(minutes=30)

    def __str__(self):
        return f"{self.user} | {self.token}"