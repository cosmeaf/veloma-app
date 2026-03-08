# authentication/models/login_event.py

from django.conf import settings
from django.db import models


class LoginEvent(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    ip = models.GenericIPAddressField(null=True, blank=True)

    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    asn = models.CharField(max_length=100, null=True, blank=True)

    browser = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    device = models.CharField(max_length=50, null=True, blank=True)

    risk_score = models.IntegerField(default=0)

    success = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "login_events"
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["ip"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.user} | {self.ip}"