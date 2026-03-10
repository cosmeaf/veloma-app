from rest_framework import serializers

from authentication.services.ip_intelligence_service import IPIntelligenceService
from consents.services.request_ip_service import RequestIPService

from .models import (
    ConsentTerm,
    ConsentVersion,
    UserConsent,
)


class ConsentTermSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConsentTerm
        fields = "__all__"


class ConsentVersionSerializer(serializers.ModelSerializer):

    term_title = serializers.CharField(
        source="term.title",
        read_only=True
    )

    class Meta:

        model = ConsentVersion

        fields = (
            "id",
            "term",
            "term_title",
            "version",
            "content",
            "document_hash",
            "active",
            "created_at",
        )

        read_only_fields = ("document_hash",)


class UserConsentSerializer(serializers.ModelSerializer):

    # declarar explicitamente
    term = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:

        model = UserConsent

        fields = "__all__"

        read_only_fields = (
            "user",
            "term",
            "document_hash",
            "ip",
            "country",
            "city",
            "asn",
            "isp",
            "is_proxy",
            "user_agent",
            "accepted_at",
        )

        extra_kwargs = {
            "version": {"write_only": True}
        }

    def create(self, validated_data):

        request = self.context["request"]

        version = validated_data["version"]

        # ------------------------------------------
        # Extract IP
        # ------------------------------------------

        ip = RequestIPService.get_client_ip(request)

        # ------------------------------------------
        # Run IP intelligence
        # ------------------------------------------

        intel = IPIntelligenceService.investigate(ip) or {}

        # ------------------------------------------
        # Create consent
        # ------------------------------------------

        return UserConsent.objects.create(

            user=request.user,

            term=version.term,

            version=version,

            accepted=True,

            document_hash=version.document_hash,

            ip=intel.get("ip", ip),

            country=intel.get("country"),

            city=intel.get("city"),

            asn=intel.get("asn"),

            isp=intel.get("asn_org") or intel.get("isp"),

            is_proxy=intel.get("proxy", False),

            user_agent=request.META.get("HTTP_USER_AGENT"),
        )