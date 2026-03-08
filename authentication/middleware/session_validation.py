from django.core.cache import cache
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import AuthenticationFailed

from authentication.models.user_session import UserSession
from authentication.services.session_service import SessionService


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

        session_data = cache.get(cache_key)

        # -------------------------------------------------
        # CACHE MISS
        # -------------------------------------------------

        if not session_data:

            session = (
                UserSession.objects
                .select_related("user")
                .filter(
                    id=session_id,
                    user=user,
                    is_active=True,
                )
                .first()
            )

            if not session:
                raise AuthenticationFailed("Sessão inválida.")

            session_data = {
                "id": str(session.id),
                "revoked_at": session.revoked_at,
                "last_seen": session.last_seen,
                "created_at": session.created_at,
            }

            cache.set(cache_key, session_data, 300)

        else:

            session = (
                UserSession.objects
                .filter(id=session_id, user=user)
                .first()
            )

            if not session:
                cache.delete(cache_key)
                raise AuthenticationFailed("Sessão inválida.")

        # -------------------------------------------------
        # VALIDATE SESSION
        # -------------------------------------------------

        if not SessionService.validate(session):

            cache.delete(cache_key)

            raise AuthenticationFailed("Sessão expirada ou revogada.")

        # -------------------------------------------------
        # TOUCH SESSION
        # -------------------------------------------------

        SessionService.touch(session.id)

        return self.get_response(request)