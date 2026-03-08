# authentication/dto/user_dto.py
"""
DTO para manter compatibilidade exata com o payload do frontend
"""

from dataclasses import dataclass, asdict


@dataclass
class UserDTO:
    id: int
    email: str
    first_name: str = ""
    last_name: str = ""
    role: str = "user"
    is_staff: bool = False
    is_superuser: bool = False
    is_active: bool = True

    @classmethod
    def from_user(cls, user):
        role = (
            "admin" if getattr(user, "is_superuser", False)
            else "staff" if getattr(user, "is_staff", False)
            else "user"
        )

        return cls(
            id=user.id,
            email=getattr(user, "email", ""),
            first_name=getattr(user, "first_name", ""),
            last_name=getattr(user, "last_name", ""),
            role=role,
            is_staff=getattr(user, "is_staff", False),
            is_superuser=getattr(user, "is_superuser", False),
            is_active=getattr(user, "is_active", True),
        )

    @classmethod
    def build(cls, user):
        """
        Mantém compatibilidade com services existentes
        """
        return cls.from_user(user).to_dict()

    def to_dict(self):
        return asdict(self)