# authentication/views/otp_verify.py

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers.otp_verify import OtpVerifySerializer
from authentication.services.otp_service import OTPService


class OtpVerifyViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]
    serializer_class = OtpVerifySerializer

    def create(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = OTPService.verify(
            email=serializer.validated_data["email"],
            code=serializer.validated_data["code"]
        )

        return Response(
            {
                "detail": "Código verificado com sucesso.",
                "reset_token": result["reset_token"],
                "expires_in": result["expires_in"]
            },
            status=status.HTTP_200_OK
        )