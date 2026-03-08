# authentication/services/login_audit_service.py

from authentication.models.login_event import LoginEvent
from services.middleware.request_context import get_login_context


class LoginAuditService:

    @staticmethod
    def register(request, user, success):

        ctx = get_login_context(request)

        LoginEvent.objects.create(
            user=user,
            ip=ctx.get("ip"),
            country=ctx.get("country"),
            city=ctx.get("city"),
            browser=ctx.get("browser"),
            os=ctx.get("os"),
            device=ctx.get("device"),
            risk_score=ctx.get("risk_score", 0),
            success=success
        )