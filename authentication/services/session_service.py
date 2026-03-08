# authentication/services/session_service.py

from authentication.models.user_session import UserSession


class SessionService:

    @staticmethod
    def create(user, jti, ctx, request):

        return UserSession.objects.create(
            user=user,
            token_jti=jti,
            ip_address=ctx.get("ip"),
            browser=ctx.get("browser"),
            os=ctx.get("os"),
            device=ctx.get("device"),
            country=ctx.get("country"),
            city=ctx.get("city"),
            asn=ctx.get("asn"),
            risk_score=ctx.get("risk_score", 0),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )

    @staticmethod
    def revoke(session_id, user):

        UserSession.objects.filter(
            id=session_id,
            user=user,
        ).update(is_active=False)