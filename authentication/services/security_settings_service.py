# authentication/services/security_settings_service.py

from authentication.models.security_settings import SecuritySettings


class SecuritySettingsService:

    @staticmethod
    def get(user):

        settings, _ = SecuritySettings.objects.get_or_create(
            user=user
        )

        return settings