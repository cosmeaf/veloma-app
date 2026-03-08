# authentication/models/login_attempt.py

from django.db import models
from django.utils import timezone


class LoginAttempt(models.Model):

    email = models.EmailField()
    ip_address = models.GenericIPAddressField()

    attempts = models.PositiveIntegerField(default=0)

    blocked_until = models.DateTimeField(null=True, blank=True)

    last_attempt_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-last_attempt_at"]

        indexes = [
            models.Index(fields=["email", "ip_address"]),
            models.Index(fields=["blocked_until"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["email", "ip_address"],
                name="unique_login_attempt_per_ip_email",
            )
        ]

    def is_blocked(self):
        return bool(self.blocked_until and timezone.now() < self.blocked_until)

    def __str__(self):
        return f"{self.email} | {self.ip_address} | {self.attempts}"