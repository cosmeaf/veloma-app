# authentication/views/me.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class MeViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):

        user = request.user

        role = "user"

        if user.is_superuser:
            role = "superuser"
        elif user.is_staff:
            role = "staff"

        return Response({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": role,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active,
            "permissions": list(user.get_all_permissions()),
        })