import os
import markdown

from django.conf import settings
from django.shortcuts import render
from django.http import Http404


DOCS_PATH = os.path.join(settings.BASE_DIR, "docs_content")


def build_sidebar():

    modules = []

    if not os.path.exists(DOCS_PATH):
        return modules

    for module in sorted(os.listdir(DOCS_PATH)):

        module_path = os.path.join(DOCS_PATH, module)

        if not os.path.isdir(module_path):
            continue

        pages = []

        for f in sorted(os.listdir(module_path)):

            if f.endswith(".md"):
                pages.append(f.replace(".md", ""))

        modules.append({
            "name": module,
            "pages": pages
        })

    return modules


def docs_index(request):

    modules = build_sidebar()

    return render(
        request,
        "docs/index.html",
        {
            "modules": modules
        }
    )


def docs_page(request, module, page):

    modules = build_sidebar()

    file_path = os.path.join(
        DOCS_PATH,
        module,
        f"{page}.md"
    )

    if not os.path.exists(file_path):
        raise Http404("Documento não encontrado")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    html = markdown.markdown(
        content,
        extensions=[
            "fenced_code",
            "tables"
        ]
    )

    return render(
        request,
        "docs/page.html",
        {
            "modules": modules,
            "title": page,
            "content": html
        }
    )