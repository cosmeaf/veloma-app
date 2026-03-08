# authentication/services/device_service.py

import hashlib

from authentication.models.user_device import UserDevice


class DeviceService:

    @staticmethod
    def fingerprint(ctx):

        raw = f"{ctx.get('browser')}-{ctx.get('os')}-{ctx.get('device')}"
        return hashlib.sha256(raw.encode()).hexdigest()

    @staticmethod
    def register(user, ctx):

        fingerprint = DeviceService.fingerprint(ctx)

        device, _ = UserDevice.objects.get_or_create(
            user=user,
            fingerprint=fingerprint,
            defaults={
                "browser": ctx.get("browser"),
                "os": ctx.get("os"),
                "device": ctx.get("device"),
            }
        )

        return device