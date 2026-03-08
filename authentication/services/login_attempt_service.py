# authentication/services/login_attempt_service.py

from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from authentication.models.login_attempt import LoginAttempt


class LoginAttemptService:

    MAX_ATTEMPTS = 5
    BLOCK_MINUTES = 15

    @staticmethod
    def guard(email, ip):

        attempt, _ = LoginAttempt.objects.get_or_create(
            email=email,
            ip_address=ip
        )

        if attempt.is_blocked():
            raise ValidationError("Muitas tentativas. Tente novamente mais tarde.")

    @staticmethod
    def register_failure(email, ip):

        attempt, _ = LoginAttempt.objects.get_or_create(
            email=email,
            ip_address=ip
        )

        attempt.attempts += 1

        if attempt.attempts >= LoginAttemptService.MAX_ATTEMPTS:
            attempt.blocked_until = timezone.now() + timedelta(
                minutes=LoginAttemptService.BLOCK_MINUTES
            )

        attempt.save()

    @staticmethod
    def reset_attempts(email, ip):

        LoginAttempt.objects.filter(
            email=email,
            ip_address=ip
        ).update(
            attempts=0,
            blocked_until=None
        )