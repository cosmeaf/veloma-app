from django.conf import settings
from django.db import models


class SecuritySettings(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="security_settings",
    )

    # SESSION POLICY

    max_devices = models.PositiveSmallIntegerField(
        default=3
    )

    max_sessions_per_device = models.PositiveSmallIntegerField(
        default=2
    )

    idle_session_timeout_minutes = models.PositiveIntegerField(
        default=1440
    )

    absolute_session_timeout_minutes = models.PositiveIntegerField(
        default=10080
    )

    # SECURITY

    otp_enabled = models.BooleanField(default=False)
    require_otp_for_new_device = models.BooleanField(default=False)

    block_high_risk_login = models.BooleanField(default=False)

    max_risk_score = models.PositiveIntegerField(default=70)

    allowed_countries = models.JSONField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "security_settings"

    def __str__(self):
        return f"{self.user}"