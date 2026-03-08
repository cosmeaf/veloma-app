from smtplib import SMTPException, SMTPDataError

from celery import shared_task
from django.core.mail import EmailMultiAlternatives

import logging

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    name="services.tasks.send_email_task",
    autoretry_for=(SMTPException,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_kwargs={"max_retries": 5},
)
def send_email_task(self, payload):

    try:

        msg = EmailMultiAlternatives(
            subject=payload["subject"],
            body=payload["text"],
            from_email=payload["from_email"],
            to=payload["to"],
            cc=payload.get("cc", []),
            bcc=payload.get("bcc", []),
        )

        if payload.get("html"):
            msg.attach_alternative(payload["html"], "text/html")

        for attachment in payload.get("attachments", []):
            filename, content, mimetype = attachment
            msg.attach(filename, content, mimetype)

        msg.send()

        logger.info(
            "Email enviado",
            extra={"to": payload["to"], "subject": payload["subject"]}
        )

    except SMTPDataError as exc:

        logger.warning(
            "SMTP bloqueou envio (rate limit Zoho)",
            extra={"error": str(exc)}
        )

        raise exc