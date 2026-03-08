# authentication/models/login_event.py

from django.conf import settings
from django.db import models


class LoginEvent(models.Model):

    # ------------------------------------------------
    # USER
    # ------------------------------------------------

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    # ------------------------------------------------
    # NETWORK
    # ------------------------------------------------

    ip = models.GenericIPAddressField(null=True, blank=True)

    country = models.CharField(max_length=100, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)

    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    timezone = models.CharField(max_length=50, null=True, blank=True)

    # ------------------------------------------------
    # NETWORK INTEL
    # ------------------------------------------------

    asn = models.CharField(max_length=100, null=True, blank=True)
    isp = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)

    vpn = models.BooleanField(null=True)
    tor = models.BooleanField(null=True)
    proxy = models.BooleanField(null=True)

    # ------------------------------------------------
    # DEVICE
    # ------------------------------------------------

    browser = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    device = models.CharField(max_length=50, null=True, blank=True)

    user_agent = models.TextField(null=True, blank=True)

    # ------------------------------------------------
    # SESSION
    # ------------------------------------------------

    session_id = models.CharField(max_length=100, null=True, blank=True)
    token_jti = models.CharField(max_length=255, null=True, blank=True)

    # ------------------------------------------------
    # SECURITY
    # ------------------------------------------------

    risk_score = models.IntegerField(default=0)

    success = models.BooleanField(default=False)

    # ------------------------------------------------
    # TIMESTAMP
    # ------------------------------------------------

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        db_table = "login_events"

        ordering = ["-created_at"]

        indexes = [

            models.Index(fields=["user"]),
            models.Index(fields=["ip"]),
            models.Index(fields=["created_at"]),

            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["ip", "created_at"]),

        ]

    def __str__(self):

        return f"{self.user} | {self.ip} | {self.created_at}"