import hashlib
import logging
from datetime import timedelta

from django.utils import timezone

from authentication.models.user_session import UserSession

logger = logging.getLogger(__name__)


class SessionService:

    # -------------------------------------------------
    # DEVICE HASH
    # -------------------------------------------------

    @staticmethod
    def build_device_hash(ctx):

        raw = "|".join([
            str(ctx.get("ip", "")),
            str(ctx.get("browser", "")),
            str(ctx.get("os", "")),
            str(ctx.get("device", "")),
        ])

        return hashlib.sha256(raw.encode()).hexdigest()

    # -------------------------------------------------
    # SESSION LIMIT
    # -------------------------------------------------

    @staticmethod
    def enforce_limit(user):

        settings = getattr(user, "security_settings", None)

        if not settings:
            return

        max_sessions = settings.max_devices

        sessions = (
            UserSession.objects
            .filter(user=user, is_active=True)
            .order_by("last_seen")
        )

        total = sessions.count()

        if total < max_sessions:
            return

        revoke_count = total - max_sessions + 1

        for session in sessions[:revoke_count]:

            try:
                session.revoke()

                logger.info(
                    "Session revoked automatically | user=%s session=%s",
                    user.id,
                    session.id
                )

            except Exception:
                logger.exception("Error revoking session")

    # -------------------------------------------------
    # CREATE SESSION
    # -------------------------------------------------

    @staticmethod
    def create(user, jti, ctx, request):

        try:

            SessionService.enforce_limit(user)

            device_hash = SessionService.build_device_hash(ctx)

            session = UserSession.objects.create(

                user=user,

                token_jti=jti,

                device_hash=device_hash,

                ip_address=ctx.get("ip"),

                country=ctx.get("country"),

                browser=ctx.get("browser"),

                os=ctx.get("os"),

                device=ctx.get("device"),

                risk_score=ctx.get("risk_score", 0),

            )

            return session

        except Exception:

            logger.exception("Failed to create session")

            raise

    # -------------------------------------------------
    # REVOKE ALL SESSIONS
    # -------------------------------------------------

    @staticmethod
    def revoke_all(user):

        sessions = UserSession.objects.filter(
            user=user,
            is_active=True
        )

        for session in sessions:
            session.revoke()

    # -------------------------------------------------
    # REVOKE OTHER SESSIONS
    # -------------------------------------------------

    @staticmethod
    def revoke_others(user, current_session_id):

        sessions = (
            UserSession.objects
            .filter(user=user, is_active=True)
            .exclude(id=current_session_id)
        )

        for session in sessions:
            session.revoke()

    # -------------------------------------------------
    # TOUCH SESSION
    # -------------------------------------------------

    @staticmethod
    def touch(session_id):

        try:

            session = UserSession.objects.get(
                id=session_id,
                is_active=True
            )

        except UserSession.DoesNotExist:
            return

        except Exception:
            logger.exception("Session lookup failed")
            return

        now = timezone.now()

        if (now - session.last_seen).seconds < 60:
            return

        session.last_seen = now

        session.save(update_fields=["last_seen"])

    # -------------------------------------------------
    # VALIDATE SESSION
    # -------------------------------------------------

    @staticmethod
    def validate(session):

        if not session.is_active:
            return False

        if session.revoked_at:
            return False

        settings = getattr(session.user, "security_settings", None)

        if not settings:
            return True

        now = timezone.now()

        # absolute timeout

        if settings.absolute_session_timeout_minutes:

            limit = timedelta(
                minutes=settings.absolute_session_timeout_minutes
            )

            if now - session.created_at > limit:

                session.revoke()

                return False

        # idle timeout

        if settings.idle_session_timeout_minutes:

            limit = timedelta(
                minutes=settings.idle_session_timeout_minutes
            )

            if now - session.last_seen > limit:

                session.revoke()

                return False

        return True