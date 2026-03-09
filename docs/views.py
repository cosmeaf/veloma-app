import os
import markdown

from django.conf import settings
from django.shortcuts import render
from django.http import Http404

DOCS_PATH = os.path.join(settings.BASE_DIR, "docs_content")

# ─── MAPA DE ÍCONES (SCALABILITY) ───
# Adicione novas chaves conforme cria novas pastas de documentação
ICON_MAP = {
    "retail": "fa-store",
    "authentication": "fa-shield-halved",
    "security": "fa-lock",
    "developers": "fa-code",
    "api": "fa-plug",
    "general": "fa-book-open",
    # Fallback padrão será 'fa-folder'
}

def get_module_icon(module_name):
    """Retorna o ícone do Font Awesome baseado no nome da pasta (case insensitive)"""
    key = module_name.lower()
    return ICON_MAP.get(key, "fa-folder")


def build_sidebar(active_module=None, active_page=None):
    """
    Constrói a sidebar com estados de UI (Aberto/Fechado) e Ícones.
    """
    modules = []

    if not os.path.exists(DOCS_PATH):
        return modules

    # Varre as pastas (Módulos)
    for module in sorted(os.listdir(DOCS_PATH)):
        module_path = os.path.join(DOCS_PATH, module)

        if not os.path.isdir(module_path):
            continue

        pages = []
        
        # Lógica: A pasta deve estar aberta se o usuário estiver navegando nela
        is_open = (module == active_module)
        
        # Pega o ícone específico para este módulo
        module_icon = get_module_icon(module)

        # Varre os arquivos (Páginas)
        for f in sorted(os.listdir(module_path)):
            if f.endswith(".md"):
                page_name = f.replace(".md", "")
                
                # Lógica: O link está ativo se for a página atual
                is_active = (page_name == active_page)

                pages.append({
                    "name": page_name,
                    "is_active": is_active
                })

        modules.append({
            "name": module,
            "icon": module_icon,     # NOVO: Ícone dinâmico
            "is_open": is_open,
            "pages": pages
        })

    return modules


def docs_index(request):
    modules = build_sidebar()
    return render(request, "docs/index.html", {"modules": modules})


def docs_page(request, module, page):
    # Passa contexto ativo para highlight automático
    modules = build_sidebar(active_module=module, active_page=page)

    file_path = os.path.join(DOCS_PATH, module, f"{page}.md")

    if not os.path.exists(file_path):
        raise Http404("Documento não encontrado")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extensões úteis para docs modernos
    html = markdown.markdown(
        content,
        extensions=[
            "fenced_code",
            "tables",
            "toc",  # Table of Contents
            "attr_list" # Permite adicionar classes aos elementos markdown
        ]
    )

    # Formatação do Título (ex: "user-auth" -> "User Auth")
    display_title = page.replace("-", " ").replace("_", " ").title()

    return render(
        request,
        "docs/page.html",
        {
            "modules": modules,
            "title": display_title,
            "content": html
        }
    )