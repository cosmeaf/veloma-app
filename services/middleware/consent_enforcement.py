from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from consents.models import ConsentTerm, UserConsent


EXCLUDED_PATHS = [

    "/api/v1/auth/login",
    "/api/v1/auth/register",
    "/api/v1/auth/refresh",

    "/api/v1/consent-terms",
    "/api/v1/consent-versions",
    "/api/v1/user-consents",
    "/api/v1/user-consents/status",

    "/admin",
]


class ConsentEnforcementMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):

        path = request.path

        # Ignorar endpoints públicos
        for p in EXCLUDED_PATHS:
            if path.startswith(p):
                return self.get_response(request)

        # Autenticar JWT manualmente
        try:
            user_auth_tuple = self.jwt_auth.authenticate(request)
        except Exception:
            user_auth_tuple = None

        if user_auth_tuple is None:
            return self.get_response(request)

        user, _ = user_auth_tuple
        request.user = user

        # staff bypass
        if user.is_staff or user.is_superuser:
            return self.get_response(request)

        required_terms = ConsentTerm.objects.filter(
            required=True,
            active=True
        )

        missing = []

        for term in required_terms:

            latest = term.versions.filter(
                active=True
            ).order_by("-created_at").first()

            if not latest:
                continue

            accepted = UserConsent.objects.filter(
                user=user,
                version=latest
            ).exists()

            if not accepted:
                missing.append(term.slug)

        if missing:

            return JsonResponse({
                "error": "consent_required",
                "missing_terms": missing
            }, status=403)

        return self.get_response(request)