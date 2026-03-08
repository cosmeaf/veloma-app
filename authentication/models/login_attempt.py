# authentication/models/login_attempt.py

from django.db import models
from django.utils import timezone


class LoginAttempt(models.Model):

    # ------------------------------------------------
    # IDENTIFICATION
    # ------------------------------------------------

    email = models.EmailField()
    ip_address = models.GenericIPAddressField()

    # ------------------------------------------------
    # SECURITY DATA
    # ------------------------------------------------

    attempts = models.PositiveIntegerField(default=0)

    blocked_until = models.DateTimeField(null=True, blank=True)

    # ------------------------------------------------
    # CONTEXT
    # ------------------------------------------------

    user_agent = models.TextField(null=True, blank=True)

    country = models.CharField(max_length=100, null=True, blank=True)

    risk_score = models.IntegerField(default=0)

    # ------------------------------------------------
    # TIMESTAMPS
    # ------------------------------------------------

    last_attempt_at = models.DateTimeField(auto_now=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # ------------------------------------------------
    # META
    # ------------------------------------------------

    class Meta:

        ordering = ["-last_attempt_at"]

        indexes = [

            models.Index(fields=["email"]),

            models.Index(fields=["ip_address"]),

            models.Index(fields=["email", "ip_address"]),

            models.Index(fields=["blocked_until"]),

            models.Index(fields=["last_attempt_at"]),

        ]

        constraints = [

            models.UniqueConstraint(
                fields=["email", "ip_address"],
                name="unique_login_attempt_per_ip_email",
            )

        ]

    # ------------------------------------------------
    # METHODS
    # ------------------------------------------------

    def is_blocked(self):

        return bool(
            self.blocked_until and timezone.now() < self.blocked_until
        )

    def __str__(self):

        return f"{self.email} | {self.ip_address} | {self.attempts}"