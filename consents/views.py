from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    ConsentTerm,
    ConsentVersion,
    UserConsent
)

from .serializers import (
    ConsentTermSerializer,
    ConsentVersionSerializer,
    UserConsentSerializer
)


class ConsentTermViewSet(viewsets.ModelViewSet):

    queryset = ConsentTerm.objects.all()

    serializer_class = ConsentTermSerializer

    permission_classes = [IsAuthenticated]


class ConsentVersionViewSet(viewsets.ModelViewSet):

    queryset = ConsentVersion.objects.select_related("term")

    serializer_class = ConsentVersionSerializer

    permission_classes = [IsAuthenticated]


class UserConsentViewSet(viewsets.ModelViewSet):

    queryset = UserConsent.objects.select_related(
        "user",
        "term",
        "version"
    )

    serializer_class = UserConsentSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        if user.is_staff or user.is_superuser:

            return self.queryset

        return self.queryset.filter(user=user)

    @action(
        detail=False,
        methods=["get"],
        url_path="status"
    )
    def status(self, request):

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
                user=request.user,
                version=latest
            ).exists()

            if not accepted:
                missing.append(term.slug)

        return Response({

            "accepted_all": len(missing) == 0,

            "missing_terms": missing

        })
    

    @action(detail=False, methods=["get"], url_path="debug-intel")
    def debug_intel(self, request):

        intel = getattr(request, "intel", None)

        if not intel:
            return Response({"intel": "NOT FOUND"})

        return Response({
            "ip": getattr(intel, "ip", None),
            "country": getattr(intel, "country", None),
            "city": getattr(intel, "city", None),
            "asn": getattr(intel, "asn", None),
            "isp": getattr(intel, "isp", None),
            "is_proxy": getattr(intel, "is_proxy", None),
            "user_agent": getattr(intel, "user_agent", None),
        })