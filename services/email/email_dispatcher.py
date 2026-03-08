import logging
import hashlib

from django.core.cache import cache

from .exceptions import EmailDispatchError

logger = logging.getLogger(__name__)


class EmailDispatcher:

    DEDUP_SECONDS = 60

    @staticmethod
    def dispatch(payload):

        try:

            # fingerprint para evitar email duplicado
            fingerprint = hashlib.sha256(
                f"{payload['subject']}:{payload['to']}".encode()
            ).hexdigest()

            cache_key = f"email_dedup:{fingerprint}"

            if cache.get(cache_key):

                logger.warning(
                    "Email duplicado bloqueado",
                    extra={
                        "subject": payload["subject"],
                        "to": payload["to"]
                    }
                )

                return None

            cache.set(cache_key, True, EmailDispatcher.DEDUP_SECONDS)

            from services.tasks import send_email_task

            result = send_email_task.delay(payload)

            logger.info(
                "Email enviado para fila Celery",
                extra={
                    "task_id": result.id,
                    "subject": payload["subject"],
                    "to": payload["to"]
                }
            )

            return result.id

        except Exception as exc:

            logger.error(
                "Erro ao enfileirar email",
                exc_info=True
            )

            raise EmailDispatchError("Falha ao enviar email") from exc