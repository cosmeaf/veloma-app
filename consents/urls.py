from rest_framework.routers import DefaultRouter

from .views import (
    ConsentTermViewSet,
    ConsentVersionViewSet,
    UserConsentViewSet
)

router = DefaultRouter()

router.register(r"consent-terms", ConsentTermViewSet)
router.register(r"consent-versions", ConsentVersionViewSet)
router.register(r"user-consents", UserConsentViewSet)

urlpatterns = router.urls