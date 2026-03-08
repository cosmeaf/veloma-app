import logging
from datetime import datetime, UTC

from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError

from authentication.dto.user_dto import UserDTO
from authentication.services.session_service import SessionService
from authentication.services.token_service import TokenService
from authentication.services.ip_intelligence_service import IPIntelligenceService
from authentication.services.login_attempt_service import LoginAttemptService
from authentication.services.login_audit_service import LoginAuditService
from authentication.services.login_security_service import LoginSecurityService

from services.middleware.request_context import get_login_context

logger = logging.getLogger(__name__)


class AuthService:

    @staticmethod
    def login(email: str, password: str, request):

        email = (email or "").lower().strip()

        # -------------------------------------------------
        # REQUEST CONTEXT
        # -------------------------------------------------

        ctx = get_login_context(request) or {}
        ip = ctx.get("ip")

        # -------------------------------------------------
        # IP INTELLIGENCE
        # -------------------------------------------------

        if ip:
            try:
                ctx.update(IPIntelligenceService.investigate(ip))
            except Exception:
                logger.exception("Falha ao investigar IP")

        # -------------------------------------------------
        # BRUTE FORCE PROTECTION
        # -------------------------------------------------

        LoginAttemptService.guard(email=email, ip=ip)

        # -------------------------------------------------
        # AUTHENTICATION
        # -------------------------------------------------

        user = authenticate(
            request=request,
            username=email,
            password=password,
        )

        if not user:

            LoginAttemptService.register_failure(email=email, ip=ip)

            LoginAuditService.register(
                request=request,
                user=None,
                success=False,
            )

            raise ValidationError("Credenciais inválidas.")

        if not user.is_active:

            LoginAuditService.register(
                request=request,
                user=user,
                success=False,
            )

            raise ValidationError("Conta desativada.")

        LoginAttemptService.reset_attempts(email=email, ip=ip)

        # -------------------------------------------------
        # CREATE TOKENS
        # -------------------------------------------------

        tokens = TokenService.create(user, None)

        # -------------------------------------------------
        # CREATE SESSION
        # -------------------------------------------------

        session = SessionService.create(
            user=user,
            jti=tokens.get("jti"),
            ctx=ctx,
            request=request,
        )

        # -------------------------------------------------
        # LOGIN AUDIT
        # -------------------------------------------------

        LoginAuditService.register(
            request=request,
            user=user,
            success=True,
        )

        # -------------------------------------------------
        # SECURITY CHECKS
        # -------------------------------------------------

        try:

            LoginSecurityService.check(
                user,
                {
                    "user": user,
                    "user_id": user.id,
                    "user_email": user.email,
                    "session_id": session.id,
                    "token_jti": tokens.get("jti"),
                    "login_time": datetime.now(UTC),
                    **ctx,
                }
            )

        except Exception:
            logger.exception("Falha ao executar verificação de segurança")

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "user": UserDTO.build(user),
        }