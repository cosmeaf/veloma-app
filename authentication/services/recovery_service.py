# authentication/services/recovery_service.py

import logging

from django.contrib.auth import get_user_model

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

        otp = OtpCode.objects.create(
            user=user,
            code=OtpCode.generate_code()
        )

        try:

            EmailService.send(
                template_key="password_recovery",
                to=[user.email],
                context={
                    "user": user,
                    "otp_code": otp.code
                }
            )

        except Exception:
            logger.exception("Falha ao enviar email de recuperação")