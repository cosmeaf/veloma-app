from django.conf import settings

from .registry import EMAIL_TEMPLATES
from .email_renderer import EmailRenderer
from .email_dispatcher import EmailDispatcher


class EmailService:

    @classmethod
    def send(

        cls,

        *,
        template_key,
        to,
        context=None,
        cc=None,
        bcc=None,
        attachments=None

    ):

        if template_key not in EMAIL_TEMPLATES:

            raise ValueError(
                f"Template '{template_key}' não registrado."
            )

        template = EMAIL_TEMPLATES[template_key]

        text, html = EmailRenderer.render(

            template.template,

            context or {}
        )

        payload = {

            "subject": template.subject,

            "text": text,
            "html": html,

            "from_email": settings.DEFAULT_FROM_EMAIL,

            "to": to,
            "cc": cc or [],
            "bcc": bcc or [],

            "attachments": attachments or []
        }

        return EmailDispatcher.dispatch(payload)