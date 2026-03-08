# authentication/models/user_device.py

from django.conf import settings
from django.db import models


class UserDevice(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="devices",
    )

    fingerprint = models.CharField(max_length=255)

    browser = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    device = models.CharField(max_length=50, null=True, blank=True)

    first_seen = models.DateTimeField(auto_now_add=True)

    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "fingerprint")

    def __str__(self):
        return f"{self.user} | {self.fingerprint}"