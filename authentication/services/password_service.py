# authentication/services/password_service.py

import logging

from rest_framework.exceptions import ValidationError

from authentication.models.reset_password_token import ResetPasswordToken
from authentication.models.user_session import UserSession

from services.email.email_service import EmailService

logger = logging.getLogger(__name__)


class PasswordService:

    @staticmethod
    def reset(token, password):

        token_obj = ResetPasswordToken.objects.filter(token=token).first()

        if not token_obj:
            raise ValidationError("Token inválido.")

        if not token_obj.is_valid():
            raise ValidationError("Token expirado ou já utilizado.")

        user = token_obj.user

        user.set_password(password)
        user.save(update_fields=["password"])

        UserSession.objects.filter(user=user).update(is_active=False)

        token_obj.delete()

        try:

            EmailService.send(
                template_key="password_changed",
                to=[user.email],
                context={"user": user}
            )

        except Exception:
            logger.exception("Falha ao enviar email confirmação")