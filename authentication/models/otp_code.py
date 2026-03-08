import secrets
import hashlib
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

    code_plain = models.CharField(max_length=6)

    code_hash = models.CharField(max_length=64)

    attempts = models.PositiveSmallIntegerField(default=0)

    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["user", "is_used"]),
            models.Index(fields=["expires_at"]),
        ]

    @staticmethod
    def generate_code():
        return f"{secrets.randbelow(1000000):06d}"

    @staticmethod
    def hash_code(code):
        return hashlib.sha256(code.encode()).hexdigest()

    @classmethod
    def create_code(cls, user):

        cls.objects.filter(user=user, is_used=False).update(is_used=True)

        code = cls.generate_code()

        obj = cls.objects.create(
            user=user,
            code_plain=code,
            code_hash=cls.hash_code(code),
            expires_at=timezone.now() + timedelta(minutes=10),
        )

        return obj, code

    def verify(self, code):

        if self.is_used:
            return False

        if timezone.now() > self.expires_at:
            return False

        if self.attempts >= 5:
            return False

        self.attempts += 1

        if self.code_hash == self.hash_code(code):

            self.is_used = True

            self.save(update_fields=["is_used", "attempts"])

            return True

        self.save(update_fields=["attempts"])

        return False

    def __str__(self):
        return f"{self.user} | {self.code_plain}"