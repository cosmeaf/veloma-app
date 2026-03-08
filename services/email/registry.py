from dataclasses import dataclass
from pathlib import Path
from django.conf import settings


@dataclass
class EmailTemplate:
    subject: str
    template: str


EMAIL_TEMPLATES = {}


def _generate_subject(name: str) -> str:
    return name.replace("_", " ").capitalize()


def _discover_templates():

    base_path = Path(settings.BASE_DIR) / "templates" / "emails"

    for file in base_path.rglob("*.html"):

        relative = file.relative_to(base_path)

        template_path = relative.with_suffix("").as_posix()

        key = relative.with_suffix("").as_posix().replace("/", "_")

        EMAIL_TEMPLATES[key] = EmailTemplate(
            subject=_generate_subject(key),
            template=template_path
        )


_discover_templates()