# veloma-app/authentication/services/login_security_service.py
import logging
from django.conf import settings
from services.email.email_service import EmailService

logger = logging.getLogger(__name__)


class LoginSecurityService:
    """
    Serviço responsável por verificar se um login é suspeito e enviar alerta quando necessário.
    """

    @staticmethod
    def check(user, ctx):
        """
        Executa a verificação de segurança do login.
        :param user: Instância do modelo User
        :param ctx: Dicionário com contexto do login (ip, country, browser, etc.)
        """
        if settings.DEBUG:
            logger.info(
                "Ambiente DEBUG → pulando verificação de login suspeito",
                extra={"user_id": user.id, "email": user.email}
            )
            return

        logger.info(
            "Iniciando verificação de segurança de login",
            extra={
                "user_id": user.id,
                "email": user.email,
                "ip": ctx.get("ip"),
                "country": ctx.get("country"),
                "browser": ctx.get("browser"),
            }
        )

        if LoginSecurityService.is_postman_or_testing_tool(ctx):
            logger.info(
                "Login detectado como ferramenta de teste (Postman/Insomnia/etc) → liberado",
                extra={"user_id": user.id, "user_agent": ctx.get("user_agent", "não informado")}
            )
            return

        if LoginSecurityService.suspicious(user, ctx):
            logger.warning(
                "Login classificado como SUSPEITO",
                extra={
                    "user_id": user.id,
                    "email": user.email,
                    "ctx": ctx
                }
            )
            LoginSecurityService.send_alert(user, ctx)
        else:
            logger.info(
                "Login considerado NORMAL/seguro",
                extra={"user_id": user.id, "email": user.email}
            )

    @staticmethod
    def is_postman_or_testing_tool(ctx):
        """Verifica se o request vem de Postman, Insomnia, Thunder Client, etc."""
        user_agent = (ctx.get("user_agent") or "").lower()
        testing_signatures = [
            "postman", "insomnia", "thunder client", "hoppscotch", "restlet",
            "httpie", "curl", "python-requests", "axios", "okhttp"
        ]
        return any(sig in user_agent for sig in testing_signatures)

    @staticmethod
    def suspicious(user, ctx):
        """
        Decide se o login atual é suspeito comparando com logins anteriores.
        Retorna True se suspeito.
        """
        ip = ctx.get("ip")
        country = ctx.get("country")
        browser = ctx.get("browser")
        os = ctx.get("os")
        device = ctx.get("device")
        risk_score = ctx.get("risk_score", 0)
        vpn_tor_proxy = ctx.get("vpn") or ctx.get("tor") or ctx.get("proxy")

        logger.debug(
            "Dados do contexto para análise de suspeita",
            extra={
                "ip": ip,
                "country": country,
                "browser": browser,
                "os": os,
                "device": device,
                "risk_score": risk_score,
                "vpn_tor_proxy": vpn_tor_proxy,
            }
        )

        # Pega os 2 últimos logins bem-sucedidos (excluindo o atual, que ainda não foi salvo)
        recent_events = list(
            user.loginevent_set
            .filter(success=True)
            .order_by("-created_at")[:2]
        )

        if len(recent_events) < 2:
            logger.info(
                "Menos de 2 logins anteriores → não é possível detectar mudança → considerado seguro",
                extra={"user_id": user.id, "event_count": len(recent_events)}
            )
            return False

        previous = recent_events[1]  # o penúltimo (o mais antigo dos dois)

        changes = []

        if previous.country != country:
            changes.append(f"país: {previous.country} → {country}")
        if previous.ip != ip:
            changes.append(f"IP: {previous.ip} → {ip}")
        if previous.browser != browser:
            changes.append(f"browser: {previous.browser} → {browser}")
        if previous.os != os:
            changes.append(f"OS: {previous.os} → {os}")
        if previous.device != device:
            changes.append(f"device: {previous.device} → {device}")

        if changes:
            logger.info(
                f"Mudanças detectadas em relação ao login anterior: {', '.join(changes)}",
                extra={"user_id": user.id}
            )

        if changes or risk_score >= 70 or vpn_tor_proxy:
            return True

        return False

    @staticmethod
    def send_alert(user, ctx):
        """Envia email de alerta de login suspeito."""
        logger.warning(
            "Enviando alerta de login suspeito por email",
            extra={
                "user_id": user.id,
                "email": user.email,
                "ip": ctx.get("ip"),
                "country": ctx.get("country"),
                "browser": ctx.get("browser"),
                "risk_score": ctx.get("risk_score"),
            }
        )

        try:
            EmailService.send(
                template_key="login_alert",
                to=[user.email],
                context={
                    "user": user,
                    **ctx
                }
            )
            logger.info("Alerta de login suspeito enviado com sucesso")
        except Exception as e:
            logger.exception(
                "Falha ao enviar alerta de login suspeito",
                extra={"user_id": user.id, "error": str(e)}
            )