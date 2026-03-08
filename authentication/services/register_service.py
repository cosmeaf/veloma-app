# authentication/services/register_service.py

import logging
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from services.email.email_service import EmailService
from authentication.dto.user_dto import UserDTO
from authentication.services.token_service import TokenService
from authentication.services.session_service import SessionService

User = get_user_model()

logger = logging.getLogger(__name__)


class RegisterService:

    @staticmethod
    def register(data):

        email = data["email"].lower().strip()

        password = data["password"]

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
        )

        group, _ = Group.objects.get_or_create(name="user")
        user.groups.add(group)

        try:

            EmailService.send(
                template_key="welcome",
                to=[user.email],
                context={
                    "user": user,
                    "year": datetime.now().year
                }
            )

        except Exception:
            logger.exception("Falha ao enviar email de boas-vindas")

        tokens = TokenService.create(user, "register")

        return {
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "user": UserDTO.build(user)
        }