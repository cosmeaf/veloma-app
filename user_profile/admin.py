from django.contrib import admin

from .models import (
    Person,
    UserProfile
)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "nif",
        "phone",
        "created_at"
    )

    search_fields = ("name", "nif")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "person",
        "onboarding_completed",
        "created_at"
    )

    search_fields = ("user__username",)