from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.exceptions import ValidationError

from authentication.models.otp_code import OtpCode
from authentication.models.reset_password_token import ResetPasswordToken

User = get_user_model()


class OTPService:

    @staticmethod
    def verify(email, code):

        user = User.objects.filter(email__iexact=email).first()

        if not user:
            raise ValidationError("Código inválido ou e-mail não encontrado.")

        otp = (
            OtpCode.objects
            .filter(user=user, is_used=False)
            .order_by("-created_at")
            .first()
        )

        if not otp:
            raise ValidationError("Código não encontrado.")

        if not otp.verify(code):
            raise ValidationError("Código inválido ou expirado.")

        with transaction.atomic():

            reset_token = ResetPasswordToken.objects.create(user=user)

        return {
            "reset_token": str(reset_token.token),
            "expires_in": 3600
        }