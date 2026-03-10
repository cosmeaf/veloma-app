from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):

    queryset = UserProfile.objects.select_related(
        "user",
        "person"
    )

    serializer_class = UserProfileSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        if user.is_staff or user.is_superuser:

            return self.queryset

        return self.queryset.filter(user=user)