# authentication/views/__init__.py

from .login import LoginViewSet
from .register import RegisterViewSet
from .logout import LogoutViewSet
from .recovery import RecoveryViewSet
from .otp_verify import OtpVerifyViewSet
from .reset_password import ResetPasswordViewSet
from .block_user import BlockUserViewSet
from .me import MeViewSet