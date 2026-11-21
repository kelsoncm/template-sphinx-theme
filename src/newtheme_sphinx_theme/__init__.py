"""{{DESCRIPTION}}"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from docutils import nodes
from sphinx.application import Sphinx

try:
    __version__ = version("newtheme-sphinx-theme")
except PackageNotFoundError:  # pragma: no cover - execução a partir do código-fonte, sem instalar
    __version__ = "0.0.0"

THEME_NAME = "newtheme_sphinx_theme"


def get_html_theme_path() -> str:
    """Retorna a pasta do tema (a que contém ``theme.toml``).

    Mantido para quem usa ``html_theme_path``; com o pacote instalado o Sphinx encontra o tema pelo *entry point*
    ``sphinx.html_themes``.
    """
    return str(Path(__file__).resolve().parent)


def _update_context(
    app: Sphinx, pagename: str, templatename: str, context: dict[str, Any], doctree: nodes.document | None
) -> None:
    """Expõe a versão do tema aos templates (rodapé)."""
    context["newtheme_version"] = __version__


def setup(app: Sphinx) -> dict[str, Any]:
    """Registra o tema no Sphinx."""
    app.add_html_theme(THEME_NAME, get_html_theme_path())
    app.connect("html-page-context", _update_context)
    return {"version": __version__, "parallel_read_safe": True, "parallel_write_safe": True}
