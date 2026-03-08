# authentication/serializers/logout.py
from rest_framework import serializers
from authentication.services.session_service import SessionService

class LogoutSerializer(serializers.Serializer):
    """
    Serializer para logout que revoga TODAS as sessões do usuário atual.
    Ideal para terminais POS, tablets, caixas etc.
    """

    all_devices = serializers.BooleanField(
        default=True,
        required=False,
        help_text="Se true (padrão), revoga todas as sessões do usuário. Se false, revoga apenas a sessão atual."
    )

    def save(self, **kwargs):
        request = self.context.get("request")
        user = request.user

        all_devices = self.validated_data.get("all_devices", True)

        if all_devices:
            # Revoga TODAS as sessões → mais seguro para POS
            revoked_count = SessionService.revoke_all(user)
            message = f"Logout realizado com sucesso. {revoked_count} sessão(ões) encerrada(s)."
        else:
            # Revoga apenas a sessão atual (comportamento original)
            token = getattr(request, "auth", None)
            if not token:
                return {"detail": "Logout realizado (sem token de autenticação)."}

            session_id = token.payload.get("session_id") if hasattr(token, "payload") else None
            if not session_id:
                return {"detail": "Logout realizado (sessão não identificada)."}

            try:
                session_uuid = uuid.UUID(str(session_id))
                SessionService.revoke(session_id=session_uuid, user=user)
                message = "Logout realizado com sucesso (apenas este dispositivo)."
            except (ValueError, TypeError):
                message = "Logout realizado (sessão inválida ou já encerrada)."

        # Opcional: você pode invalidar refresh tokens aqui, se estiver usando simplejwt
        # from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
        # OutstandingToken.objects.filter(user=user).delete()

        return {
            "detail": message,
            "all_devices": all_devices,
            "revoked_sessions": revoked_count if all_devices else 1
        }