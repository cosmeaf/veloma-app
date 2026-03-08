# authentication/views/block_user.py

from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response

from core.permissions import IsStaffOrAdmin

User = get_user_model()


class BlockUserViewSet(viewsets.ViewSet):

    permission_classes = [IsStaffOrAdmin]

    def create(self, request):

        username = request.data.get("username")

        if not username:
            return Response(
                {"detail": "O campo 'username' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            user = User.objects.get(username=username)

            if user.is_superuser:
                return Response(
                    {"detail": "Não é permitido bloquear um superusuário."},
                    status=status.HTTP_403_FORBIDDEN
                )

            user.is_active = False
            user.save(update_fields=["is_active"])

            return Response(
                {"detail": f"Usuário '{username}' bloqueado com sucesso."},
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:

            return Response(
                {"detail": "Usuário não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )