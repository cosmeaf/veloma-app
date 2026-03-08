# authentication/views/recovery.py

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers.recovery import RecoverySerializer
from authentication.services.recovery_service import RecoveryService


class RecoveryViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]
    serializer_class = RecoverySerializer

    def create(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        RecoveryService.send_otp(serializer.validated_data["email"])

        return Response(
            {"detail": "Código de recuperação enviado para o seu e-mail."},
            status=status.HTTP_200_OK
        )