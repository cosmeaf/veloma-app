# authentication/serializers/__init__.py

from .register import RegisterSerializer
from .login import LoginSerializer
from .logout import LogoutSerializer
from .recovery import RecoverySerializer
from .otp_verify import OtpVerifySerializer
from .reset_password import ResetPasswordSerializer