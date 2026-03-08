# authentication/services/device_service.py

import hashlib

from authentication.models.user_device import UserDevice


class DeviceService:

    @staticmethod
    def fingerprint(ctx):

        raw = "|".join([
            str(ctx.get("user_agent", "")),
            str(ctx.get("browser", "")),
            str(ctx.get("os", "")),
            str(ctx.get("device", "")),
        ])

        return hashlib.sha256(raw.encode()).hexdigest()


    @staticmethod
    def register(user, ctx):

        fingerprint = DeviceService.fingerprint(ctx)

        device, created = UserDevice.objects.get_or_create(
            user=user,
            fingerprint=fingerprint,
            defaults={
                "browser": ctx.get("browser"),
                "os": ctx.get("os"),
                "device": ctx.get("device"),
                "user_agent": ctx.get("user_agent"),
            }
        )

        # ------------------------------------------------
        # update metadata if device already exists
        # ------------------------------------------------

        if not created:

            updated = False

            if device.browser != ctx.get("browser"):
                device.browser = ctx.get("browser")
                updated = True

            if device.os != ctx.get("os"):
                device.os = ctx.get("os")
                updated = True

            if device.device != ctx.get("device"):
                device.device = ctx.get("device")
                updated = True

            if device.user_agent != ctx.get("user_agent"):
                device.user_agent = ctx.get("user_agent")
                updated = True

            if updated:
                device.save()

        return device