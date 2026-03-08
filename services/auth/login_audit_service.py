from authentication.models import LoginEvent


def register_login_event(request, user, success):

    ctx = getattr(request, "audit_context", {})

    LoginEvent.objects.create(
        user=user,
        ip=ctx.get("ip"),
        country=ctx.get("country"),
        city=ctx.get("city"),
        browser=ctx.get("browser"),
        os=ctx.get("os"),
        device=ctx.get("device"),
        success=success
    )