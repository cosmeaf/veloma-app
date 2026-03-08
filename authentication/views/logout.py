# authentication/views/logout.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.serializers.logout import LogoutSerializer


class LogoutViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def create(self, request):

        serializer = self.serializer_class(
            data={},
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        result = serializer.save()

        return Response(result, status=status.HTTP_200_OK)