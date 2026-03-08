import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from authentication.models.otp_code import OtpCode
from services.email.email_service import EmailService

User = get_user_model()

logger = logging.getLogger(__name__)


class RecoveryService:

    @staticmethod
    def send_otp(email):

        user = User.objects.filter(email__iexact=email).first()

        if not user:
            return

        # Rate limit: 1 OTP por minuto
        recent = OtpCode.objects.filter(
            user=user,
            created_at__gte=timezone.now() - timedelta(seconds=60)
        ).exists()

        if recent:
            logger.warning(f"OTP rate limit para {email}")
            return

        otp_obj, otp_code = OtpCode.create_code(user)

        logger.info(f"OTP gerado para {user.email}")

        try:

            EmailService.send(
                template_key="password_recovery",
                to=[user.email],
                context={
                    "user": user,
                    "otp_code": otp_code
                }
            )

        except Exception:
            logger.exception("Falha ao enviar email de recuperação")