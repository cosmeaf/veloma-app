# authentication/services/token_service.py

from rest_framework_simplejwt.tokens import RefreshToken


class TokenService:

    @staticmethod
    def create(user, session_id):

        refresh = RefreshToken.for_user(user)

        # ------------------------------------------------
        # SESSION BINDING
        # ------------------------------------------------

        if session_id:
            refresh["session_id"] = str(session_id)

        # ------------------------------------------------
        # USER META
        # ------------------------------------------------

        refresh["user_id"] = user.id

        access = refresh.access_token

        if session_id:
            access["session_id"] = str(session_id)

        access["user_id"] = user.id

        return {
            "access": str(access),
            "refresh": str(refresh),
            "jti": str(refresh["jti"]),
        }