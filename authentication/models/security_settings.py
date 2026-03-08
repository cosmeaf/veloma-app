# authentication/models/security_settings.py

from django.conf import settings
from django.db import models


class SecuritySettings(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="security_settings",
    )

    max_sessions = models.IntegerField(default=3)

    otp_enabled = models.BooleanField(default=False)

    email_alerts = models.BooleanField(default=True)

    require_otp_for_new_device = models.BooleanField(default=False)

    block_high_risk_login = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"