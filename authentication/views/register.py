# authentication/views/register.py

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers.register import RegisterSerializer
from authentication.services.register_service import RegisterService


class RegisterViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = RegisterService.register(serializer.validated_data)

        return Response(result, status=status.HTTP_201_CREATED)