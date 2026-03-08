# authentication/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

# Importar as views da nova estrutura modular
from .views.register     import RegisterViewSet
from .views.login        import LoginViewSet
from .views.logout       import LogoutViewSet
from .views.recovery     import RecoveryViewSet
from .views.otp_verify   import OtpVerifyViewSet
from .views.reset_password import ResetPasswordViewSet
from .views.block_user   import BlockUserViewSet
from .views.me           import MeViewSet

router = DefaultRouter()

# Registro dos endpoints (mantendo os mesmos basenames para não quebrar frontend/contratos)
router.register(r"register",     RegisterViewSet,     basename="auth-register")
router.register(r"login",        LoginViewSet,        basename="auth-login")
router.register(r"logout",       LogoutViewSet,       basename="auth-logout")
router.register(r"recovery",     RecoveryViewSet,     basename="auth-recovery")
router.register(r"otp-verify",   OtpVerifyViewSet,    basename="auth-otp-verify")
router.register(r"reset-password", ResetPasswordViewSet, basename="auth-reset-password")
router.register(r"block-user",   BlockUserViewSet,    basename="auth-block-user")
router.register(r"me",           MeViewSet,           basename="auth-me")

urlpatterns = [
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls