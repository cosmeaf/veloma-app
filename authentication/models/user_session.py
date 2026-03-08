# authentication/models/user_session.py

import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class UserSession(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions",
    )

    token_jti = models.CharField(max_length=255, db_index=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)

    browser = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    device = models.CharField(max_length=50, null=True, blank=True)

    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    asn = models.CharField(max_length=100, null=True, blank=True)

    risk_score = models.IntegerField(default=0)

    user_agent = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    last_seen = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["token_jti"]),
        ]

    def touch(self):
        self.last_seen = timezone.now()
        self.save(update_fields=["last_seen"])

    def revoke(self):
        self.is_active = False
        self.save(update_fields=["is_active"])

    def __str__(self):
        return f"{self.user.email} | {self.ip_address}"