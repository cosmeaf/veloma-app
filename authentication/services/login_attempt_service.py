# authentication/services/login_attempt_service.py

from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from authentication.models.login_attempt import LoginAttempt


class LoginAttemptService:

    MAX_ATTEMPTS = 5
    BLOCK_MINUTES = 15
    WINDOW_MINUTES = 10


    @staticmethod
    def guard(email, ip):

        now = timezone.now()
        window = now - timedelta(minutes=LoginAttemptService.WINDOW_MINUTES)

        # ------------------------------------------------
        # BLOCK BY EMAIL + IP
        # ------------------------------------------------

        attempt = LoginAttempt.objects.filter(
            email=email,
            ip_address=ip
        ).first()

        if attempt and attempt.is_blocked():
            raise ValidationError(
                "Muitas tentativas deste IP. Aguarde alguns minutos."
            )

        # ------------------------------------------------
        # GLOBAL EMAIL ATTACK
        # ------------------------------------------------

        email_attempts = LoginAttempt.objects.filter(
            email=email,
            created_at__gte=window
        ).count()

        if email_attempts >= LoginAttemptService.MAX_ATTEMPTS * 3:
            raise ValidationError(
                "Conta temporariamente bloqueada por segurança."
            )

        # ------------------------------------------------
        # GLOBAL IP ATTACK
        # ------------------------------------------------

        ip_attempts = LoginAttempt.objects.filter(
            ip_address=ip,
            created_at__gte=window
        ).count()

        if ip_attempts >= LoginAttemptService.MAX_ATTEMPTS * 3:
            raise ValidationError(
                "Este IP está temporariamente bloqueado."
            )


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