from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import Throttled
from authentication.models import LoginAttempt


class LoginAttemptService:

    MAX_ATTEMPTS = 5
    BLOCK_TIME_MINUTES = 15

    @classmethod
    def guard(cls, email, ip):

        attempt = LoginAttempt.objects.filter(
            email=email,
            ip_address=ip
        ).first()

        if not attempt:
            return

        if attempt.blocked_until and attempt.blocked_until > timezone.now():
            raise Throttled(
                detail="Muitas tentativas de login. Tente novamente mais tarde."
            )

        if attempt.blocked_until and attempt.blocked_until <= timezone.now():
            attempt.attempts = 0
            attempt.blocked_until = None
            attempt.save(update_fields=["attempts", "blocked_until"])


    @classmethod
    def register_failure(cls, email, ip):

        attempt, _ = LoginAttempt.objects.get_or_create(
            email=email,
            ip_address=ip
        )

        attempt.attempts += 1

        if attempt.attempts >= cls.MAX_ATTEMPTS:
            attempt.blocked_until = timezone.now() + timedelta(
                minutes=cls.BLOCK_TIME_MINUTES
            )

        attempt.save(update_fields=["attempts", "blocked_until"])


    @classmethod
    def reset_attempts(cls, email, ip):

        LoginAttempt.objects.filter(
            email=email,
            ip_address=ip
        ).update(
            attempts=0,
            blocked_until=None
        )