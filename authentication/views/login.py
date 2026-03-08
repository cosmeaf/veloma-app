# authentication/views/login.py

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers.login import LoginSerializer
from authentication.services.auth_service import AuthService


class LoginViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def create(self, request):

        serializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        result = AuthService.login(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            request=request
        )

        return Response(result, status=status.HTTP_200_OK)