from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.admin.sites import NotRegistered

from authentication.models import LoginAttempt,OtpCode,ResetPasswordToken,UserSession,LoginEvent

User=get_user_model()

try:
    admin.site.unregister(User)
except NotRegistered:
    pass


# USER SESSIONS INLINE
class UserSessionInline(admin.TabularInline):
    model=UserSession
    extra=0
    readonly_fields=("id","ip_address","browser","os","device","user_agent","created_at","last_seen","is_active")
    can_delete=False
    show_change_link=True


# USER ADMIN
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines=(UserSessionInline,)

    list_display=("id","username","email","first_name","last_name","is_active","is_staff","is_superuser","last_login","date_joined")
    search_fields=("username","email","first_name","last_name")
    list_filter=("is_active","is_staff","is_superuser","groups","date_joined","last_login")
    ordering=("-date_joined",)
    readonly_fields=("last_login","date_joined")

    actions=("activate_users","deactivate_users")

    def activate_users(self,request,queryset):
        queryset.update(is_active=True)
    activate_users.short_description="Ativar usuários selecionados"

    def deactivate_users(self,request,queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description="Desativar usuários selecionados"


# LOGIN ATTEMPTS
@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display=("email","ip_address","attempts","blocked_until","last_attempt_at","created_at")
    search_fields=("email","ip_address")
    list_filter=("blocked_until","last_attempt_at","created_at")
    ordering=("-last_attempt_at",)
    readonly_fields=("email","ip_address","attempts","blocked_until","last_attempt_at","created_at")

    actions=("clear_block",)

    def clear_block(self,request,queryset):
        queryset.update(attempts=0,blocked_until=None)
    clear_block.short_description="Limpar bloqueio e resetar tentativas"


# OTP CODES
@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display=("user","code","is_used","created_at")
    search_fields=("user__username","user__email","code")
    list_filter=("is_used","created_at")
    ordering=("-created_at",)
    readonly_fields=("user","code","is_used","created_at")

    actions=("mark_used","mark_unused")

    def mark_used(self,request,queryset):
        queryset.update(is_used=True)
    mark_used.short_description="Marcar como usados"

    def mark_unused(self,request,queryset):
        queryset.update(is_used=False)
    mark_unused.short_description="Marcar como não usados"


# PASSWORD RESET TOKENS
@admin.register(ResetPasswordToken)
class ResetPasswordTokenAdmin(admin.ModelAdmin):
    list_display=("user","token","created_at")
    search_fields=("user__username","user__email","token")
    list_filter=("created_at",)
    ordering=("-created_at",)
    readonly_fields=("user","token","created_at")

    actions=("delete_tokens",)

    def delete_tokens(self,request,queryset):
        queryset.delete()
    delete_tokens.short_description="Excluir tokens selecionados"


# USER SESSIONS
@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display=("user","ip_address","browser","device","is_active","created_at","last_seen")
    search_fields=("user__username","user__email","ip_address","token_jti","user_agent")
    list_filter=("is_active","browser","os","device","created_at")
    ordering=("-created_at",)

    readonly_fields=("id","user","token_jti","ip_address","browser","os","device","user_agent","created_at","last_seen")

    actions=("revoke_sessions","activate_sessions")

    def revoke_sessions(self,request,queryset):
        queryset.update(is_active=False)
    revoke_sessions.short_description="Revogar sessões"

    def activate_sessions(self,request,queryset):
        queryset.update(is_active=True)
    activate_sessions.short_description="Reativar sessões"


# LOGIN EVENTS
@admin.register(LoginEvent)
class LoginEventAdmin(admin.ModelAdmin):
    list_display=("user","ip","country","city","browser","os","device","success","created_at")
    search_fields=("user__username","user__email","ip","country","city","browser","os","device")
    list_filter=("success","country","browser","os","device","created_at")
    ordering=("-created_at",)
    readonly_fields=("user","ip","country","city","browser","os","device","success","created_at")