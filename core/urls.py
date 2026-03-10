from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def healthcheck(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs/", include("docs.urls")),
    path("api/v1/auth/", include("authentication.urls")),
    path("api/v1/", include("consents.urls")),
    path("api/v1/", include("user_profile.urls")),
    path("health/", healthcheck),
]
