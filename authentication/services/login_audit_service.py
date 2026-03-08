# authentication/services/login_audit_service.py

from django.utils import timezone

from authentication.models.login_event import LoginEvent
from services.middleware.request_context import get_login_context


class LoginAuditService:

    @staticmethod
    def register(request, user, success):

        ctx = get_login_context(request) or {}

        LoginEvent.objects.create(

            # ------------------------------------------------
            # USER
            # ------------------------------------------------

            user=user,

            # ------------------------------------------------
            # NETWORK
            # ------------------------------------------------

            ip=ctx.get("ip"),
            country=ctx.get("country"),
            city=ctx.get("city"),

            # ------------------------------------------------
            # DEVICE
            # ------------------------------------------------

            browser=ctx.get("browser"),
            os=ctx.get("os"),
            device=ctx.get("device"),
            user_agent=ctx.get("user_agent"),

            # ------------------------------------------------
            # NETWORK INTEL
            # ------------------------------------------------

            asn=ctx.get("asn"),
            isp=ctx.get("isp"),
            organization=ctx.get("organization"),

            vpn=ctx.get("vpn"),
            tor=ctx.get("tor"),
            proxy=ctx.get("proxy"),

            # ------------------------------------------------
            # SECURITY
            # ------------------------------------------------

            risk_score=ctx.get("risk_score", 0),

            # ------------------------------------------------
            # SESSION
            # ------------------------------------------------

            session_id=ctx.get("session_id"),
            token_jti=ctx.get("token_jti"),

            # ------------------------------------------------
            # RESULT
            # ------------------------------------------------

            success=success,

            created_at=timezone.now()
        )