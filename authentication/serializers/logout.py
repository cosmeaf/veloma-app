# authentication/serializers/logout.py

from rest_framework import serializers


class LogoutSerializer(serializers.Serializer):

    def save(self, **kwargs):

        request = self.context["request"]

        token = request.auth

        if not token:
            return {"detail": "Logout realizado."}

        session_id = token.payload.get("session_id")

        if not session_id:
            return {"detail": "Logout realizado."}

        from authentication.services.session_service import SessionService

        SessionService.revoke(
            session_id=session_id,
            user=request.user
        )

        return {"detail": "Logout realizado com sucesso."}