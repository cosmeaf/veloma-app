from authentication.models import LoginEvent


def is_suspicious_login(user, ip, country):

    last_login = LoginEvent.objects.filter(
        user=user
    ).order_by("-created_at").first()

    if not last_login:
        return False

    if last_login.ip != ip:
        return True

    if last_login.country != country:
        return True

    return False