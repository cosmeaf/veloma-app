import logging

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .exceptions import EmailTemplateError

logger = logging.getLogger(__name__)


class EmailRenderer:

    @staticmethod
    def render(template_path, context):

        try:
            html = render_to_string(f"{template_path}.html", context)

        except Exception as exc:

            logger.error(
                "Erro ao renderizar template HTML: %s",
                template_path,
                exc_info=True
            )

            raise EmailTemplateError(
                f"Template não encontrado: {template_path}.html"
            ) from exc

        try:
            text = render_to_string(f"{template_path}.txt", context)

        except Exception:
            text = strip_tags(html)

        return text, html