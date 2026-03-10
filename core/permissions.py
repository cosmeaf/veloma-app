# core/permissions.py

import logging
from rest_framework.permissions import BasePermission

logger = logging.getLogger("core.permissions")


class IsStaffOrAdmin(BasePermission):
    """
    Permite acesso apenas para:
    - is_staff
    - is_superuser

    Seguro:
    - Superuser sempre passa
    - Nunca lança exception
    - Loga inconsistências
    - Fallback seguro (nega acesso)
    """

    message = "Acesso permitido apenas para staff ou admin."

    def has_permission(self, request, view):
        try:
            user = getattr(request, "user", None)

            if not user or not user.is_authenticated:
                return False

            if user.is_superuser:
                return True

            if user.is_staff:
                return True

            logger.info(
                "Acesso negado (não staff/admin)",
                extra={
                    "user_id": getattr(user, "id", None),
                    "email": getattr(user, "email", None),
                    "path": request.path,
                    "method": request.method,
                },
            )

            return False

        except Exception:
            logger.exception(
                "Erro inesperado em IsStaffOrAdmin",
                extra={
                    "path": getattr(request, "path", None),
                },
            )
            return False

    def has_object_permission(self, request, view, obj):
        # Para esse caso macro, mesma lógica do has_permission
        return self.has_permission(request, view)


class HasRequiredPermission(BasePermission):
    """
    Permissão granular baseada em Django permissions.

    Uso:
        class MyView(APIView):
            permission_classes = [HasRequiredPermission]
            required_permission = "core.close_period"
    """

    message = "Você não possui permissão para executar esta ação."

    def has_permission(self, request, view):
        try:
            user = getattr(request, "user", None)

            if not user or not user.is_authenticated:
                return False

            if user.is_superuser:
                return True

            required_permission = getattr(view, "required_permission", None)

            if not required_permission:
                logger.warning(
                    "View sem required_permission definido",
                    extra={"view": view.__class__.__name__},
                )
                return False

            allowed = user.has_perm(required_permission)

            if not allowed:
                logger.info(
                    "Permissão negada",
                    extra={
                        "user_id": user.id,
                        "email": user.email,
                        "required_permission": required_permission,
                        "path": request.path,
                    },
                )

            return allowed

        except Exception:
            logger.exception("Erro inesperado em HasRequiredPermission")
            return False

 
class IsOwnerOrAdmin(BasePermission):
    """
    Permite acesso ao owner do objeto ou superuser.
    """

    message = "Você não tem permissão para acessar este recurso."

    def has_object_permission(self, request, view, obj):
        try:
            user = request.user

            if not user or not user.is_authenticated:
                return False

            if user.is_superuser:
                return True

            owner = getattr(obj, "owner", None)

            return owner == user

        except Exception:
            logger.exception("Erro em IsOwnerOrAdmin")
            return False       