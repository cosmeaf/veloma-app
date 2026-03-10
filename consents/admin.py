from django.contrib import admin

from .models import (
    ConsentTerm,
    ConsentVersion,
    UserConsent
)


@admin.register(ConsentTerm)
class ConsentTermAdmin(admin.ModelAdmin):

    list_display = (
        "slug",
        "title",
        "required",
        "active",
        "created_at"
    )

    search_fields = ("slug", "title")


@admin.register(ConsentVersion)
class ConsentVersionAdmin(admin.ModelAdmin):

    list_display = (
        "term",
        "version",
        "document_hash",
        "active",
        "created_at"
    )

    search_fields = ("version",)


@admin.register(UserConsent)
class UserConsentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "term",
        "version",
        "ip",
        "country",
        "created_at"
    )

    search_fields = ("user__username", "term__slug")