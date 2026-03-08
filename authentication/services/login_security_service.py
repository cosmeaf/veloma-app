# authentication/services/login_security_service.py

from services.email.email_service import EmailService


class LoginSecurityService:

    @staticmethod
    def suspicious(user, ip, country):

        last = (
            user.loginevent_set
            .filter(success=True)
            .order_by("-created_at")
            .first()
        )

        if not last:
            return False

        if last.ip != ip:
            return True

        if last.country != country:
            return True

        return False

    @staticmethod
    def send_alert(user, ctx):

        EmailService.send(
            template_key="security_login_alert",
            to=[user.email],
            context={
                "user": user,
                "ip": ctx.get("ip"),
                "country": ctx.get("country"),
                "city": ctx.get("city"),
                "browser": ctx.get("browser"),
                "os": ctx.get("os"),
                "device": ctx.get("device"),
            }
        )