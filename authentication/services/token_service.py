# authentication/services/token_service.py

from rest_framework_simplejwt.tokens import RefreshToken


class TokenService:

    @staticmethod
    def create(user, session_id):

        refresh = RefreshToken.for_user(user)

        refresh["session_id"] = str(session_id)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "jti": str(refresh["jti"]),
        }