from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.admin.sites import NotRegistered
from django.utils import timezone

from authentication.models import (
    LoginAttempt,
    OtpCode,
    ResetPasswordToken,
    SecuritySettings,
    UserSession,
    LoginEvent,
)

User = get_user_model()

# =====================================================
# UNREGISTER DEFAULT USER
# =====================================================

try:
    admin.site.unregister(User)
except NotRegistered:
    pass


# =====================================================
# USER SESSION INLINE
# =====================================================

class UserSessionInline(admin.TabularInline):

    model = UserSession
    extra = 0
    can_delete = False
    show_change_link = True
    classes = ("collapse",)

    fields = (
        "ip_address",
        "country",
        "device",
        "browser",
        "os",
        "risk_score",
        "is_active",
        "created_at",
        "last_seen",
    )

    readonly_fields = fields

    ordering = ("-created_at",)


# =====================================================
# LOGIN EVENT INLINE
# =====================================================

class LoginEventInline(admin.TabularInline):

    model = LoginEvent
    extra = 0
    can_delete = False
    show_change_link = True
    classes = ("collapse",)

    fields = (
        "ip",
        "country",
        "city",
        "browser",
        "os",
        "device",
        "success",
        "created_at",
    )

    readonly_fields = fields

    ordering = ("-created_at",)


# =====================================================
# USER ADMIN
# =====================================================

@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    inlines = (
        UserSessionInline,
        LoginEventInline,
    )

    list_display = (
        "id",
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
        "date_joined",
    )

    ordering = ("-date_joined",)

    readonly_fields = (
        "last_login",
        "date_joined",
    )

    actions = ("activate_users", "deactivate_users")

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)

    activate_users.short_description = "Ativar usuários selecionados"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)

    deactivate_users.short_description = "Desativar usuários selecionados"

# =====================================================
# SECURITY SETTINGS
# =====================================================

@admin.register(SecuritySettings)
class SecuritySettingsAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "max_devices",
        "idle_session_timeout_minutes",
        "absolute_session_timeout_minutes",
        "otp_enabled",
        "block_high_risk_login",
        "max_risk_score",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    list_filter = (
        "otp_enabled",
        "block_high_risk_login",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

# =====================================================
# USER SESSIONS
# =====================================================

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "ip_address",
        "country",
        "device",
        "browser",
        "os",
        "risk_score",
        "is_active",
        "created_at",
        "last_seen",
    )

    search_fields = (
        "user__username",
        "user__email",
        "ip_address",
        "token_jti",
        "device_hash",
    )

    list_filter = (
        "is_active",
        "browser",
        "os",
        "country",
        "created_at",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "id",
        "user",
        "token_jti",
        "device_hash",
        "ip_address",
        "country",
        "browser",
        "os",
        "device",
        "risk_score",
        "created_at",
        "last_seen",
        "revoked_at",
    )

    actions = (
        "revoke_sessions",
        "reactivate_sessions",
    )

    def revoke_sessions(self, request, queryset):

        queryset.update(
            is_active=False,
            revoked_at=timezone.now()
        )

    revoke_sessions.short_description = "Revogar sessões selecionadas"

    def reactivate_sessions(self, request, queryset):

        queryset.update(
            is_active=True,
            revoked_at=None
        )

    reactivate_sessions.short_description = "Reativar sessões"
    
# =====================================================
# LOGIN ATTEMPTS
# =====================================================

@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "ip_address",
        "attempts",
        "blocked_until",
        "last_attempt_at",
        "created_at",
    )

    search_fields = (
        "email",
        "ip_address",
    )

    list_filter = (
        "blocked_until",
        "last_attempt_at",
        "created_at",
    )

    ordering = ("-last_attempt_at",)

    readonly_fields = (
        "email",
        "ip_address",
        "attempts",
        "blocked_until",
        "last_attempt_at",
        "created_at",
    )

    actions = ("clear_block",)

    def clear_block(self, request, queryset):

        queryset.update(
            attempts=0,
            blocked_until=None
        )

    clear_block.short_description = "Limpar bloqueio"


# =====================================================
# OTP
# =====================================================

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "code_plain",
        "attempts",
        "is_used",
        "created_at",
        "expires_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    list_filter = (
        "is_used",
        "created_at",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "user",
        "code_plain",
        "code_hash",
        "attempts",
        "is_used",
        "created_at",
        "expires_at",
    )

    actions = ("mark_used", "mark_unused")

    def mark_used(self, request, queryset):
        queryset.update(is_used=True)

    mark_used.short_description = "Marcar como usados"

    def mark_unused(self, request, queryset):
        queryset.update(is_used=False)

    mark_unused.short_description = "Marcar como não usados"


# =====================================================
# PASSWORD RESET
# =====================================================

@admin.register(ResetPasswordToken)
class ResetPasswordTokenAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "token",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "token",
    )

    list_filter = (
        "created_at",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "user",
        "token",
        "created_at",
    )

    actions = ("delete_tokens",)

    def delete_tokens(self, request, queryset):
        queryset.delete()

    delete_tokens.short_description = "Excluir tokens"


# =====================================================
# LOGIN EVENTS
# =====================================================

@admin.register(LoginEvent)
class LoginEventAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "ip",
        "country",
        "city",
        "browser",
        "os",
        "device",
        "success",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "ip",
        "country",
        "city",
    )

    list_filter = (
        "success",
        "country",
        "browser",
        "os",
        "device",
        "created_at",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "user",
        "ip",
        "country",
        "city",
        "browser",
        "os",
        "device",
        "success",
        "created_at",
    )