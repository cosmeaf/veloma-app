# authentication/middleware/session_validation.py

from django.core.cache import cache
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser

from authentication.models.user_session import UserSession


class SessionValidationMiddleware:

    CACHE_PREFIX = "auth_session"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user = getattr(request, "user", AnonymousUser())

        if not user.is_authenticated:
            return self.get_response(request)

        token = getattr(request, "auth", None)

        if not token or not hasattr(token, "payload"):
            return self.get_response(request)

        session_id = token.payload.get("session_id")

        if not session_id:
            return self.get_response(request)

        cache_key = f"{self.CACHE_PREFIX}:{session_id}"

        session_valid = cache.get(cache_key)

        if session_valid is None:

            session_valid = UserSession.objects.filter(
                id=session_id,
                user=user,
                is_active=True,
            ).exists()

            cache.set(cache_key, session_valid, 300)

        if not session_valid:
            raise AuthenticationFailed("Sessão revogada.")

        return self.get_response(request)