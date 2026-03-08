# authentication/models/otp_code.py

import random
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone


class OtpCode(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otp_codes",
    )

    code = models.CharField(max_length=6)

    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "is_used"])]

    @staticmethod
    def generate_code():
        return f"{random.randint(0, 999999):06d}"

    def is_valid(self):
        return (
            not self.is_used
            and (timezone.now() - self.created_at) <= timedelta(minutes=10)
        )

    def __str__(self):
        return f"{self.user} | {self.code}"