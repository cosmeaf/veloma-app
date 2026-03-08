# authentication/services/auth_service.py

import logging
from datetime import datetime, UTC

from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError

from authentication.dto.user_dto import UserDTO
from authentication.services.session_service import SessionService
from authentication.services.token_service import TokenService
from authentication.services.ip_intelligence_service import IPIntelligenceService

from services.auth.login_attempt_service import LoginAttemptService
from services.auth.login_audit_service import register_login_event
from services.auth.login_security_service import is_suspicious_login

from services.middleware.request_context import get_login_context
from services.email.email_service import EmailService

from authentication.models.user_session import UserSession

logger = logging.getLogger(__name__)


class AuthService:

    @staticmethod
    def login(email, password, request):

        # =========================================================
        # CONTEXTO DO REQUEST
        # =========================================================

        ctx = get_login_context(request) or {}

        ip = ctx.get("ip")
        country = ctx.get("country")

        email = (email or "").lower().strip()

        # =========================================================
        # PROTEÇÃO BRUTE FORCE
        # =========================================================

        LoginAttemptService.guard(email=email, ip=ip)

        user = authenticate(
            request=request,
            username=email,
            password=password,
        )

        if not user:

            LoginAttemptService.register_failure(email=email, ip=ip)
            register_login_event(request, None, False)

            raise ValidationError("Credenciais inválidas.")

        if not user.is_active:

            register_login_event(request, user, False)

            raise ValidationError("Conta desativada.")

        LoginAttemptService.reset_attempts(email=email, ip=ip)
        register_login_event(request, user, True)

        # =========================================================
        # LIMITE DE SESSÕES
        # =========================================================

        max_sessions = getattr(user, "max_sessions", 3)

        active_sessions = UserSession.objects.filter(
            user=user,
            is_active=True,
        ).count()

        if active_sessions >= max_sessions:
            raise ValidationError("Limite de sessões simultâneas atingido.")

        # =========================================================
        # IP INTELLIGENCE
        # =========================================================

        if ip:
            try:
                ip_data = IPIntelligenceService.investigate(ip)
                if ip_data:
                    ctx.update(ip_data)
            except Exception:
                logger.exception("Falha ao investigar IP")

        # =========================================================
        # CRIAÇÃO DA SESSÃO
        # =========================================================

        session = SessionService.create(
            user=user,
            jti="temp",
            ctx=ctx,
            request=request,
        )

        tokens = TokenService.create(user, session.id)

        if tokens and "jti" in tokens:
            session.token_jti = tokens["jti"]
            session.save(update_fields=["token_jti"])

        # =========================================================
        # CONTEXTO PARA EMAIL
        # =========================================================

        email_ctx = {
            "user": user,
            "user_id": user.id,
            "user_email": user.email,
            "session_id": session.id,
            "token_jti": session.token_jti,
            "login_time": datetime.now(UTC),
            **ctx,
        }

        logger.info("Login context: %s", email_ctx)

        # =========================================================
        # EMAIL DE LOGIN
        # =========================================================

        try:
            EmailService.send(
                template_key="login_alert",
                to=[user.email],
                context=email_ctx,
            )
        except Exception:
            logger.exception("Falha ao enviar email")

        # =========================================================
        # ALERTA DE LOGIN SUSPEITO
        # =========================================================

        try:

            if is_suspicious_login(user, ip, country):

                EmailService.send(
                    template_key="security_login_alert",
                    to=[user.email],
                    context=email_ctx,
                )

        except Exception:
            logger.exception("Falha ao enviar alerta de segurança")

        # =========================================================
        # RESPONSE
        # =========================================================

        return {
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "user": UserDTO.build(user),
        }