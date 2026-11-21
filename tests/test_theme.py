"""Testes de build: o tema gera o HTML esperado em um projeto Sphinx mínimo."""

from __future__ import annotations

from pathlib import Path

from sphinx.application import Sphinx

from newtheme_sphinx_theme import THEME_NAME, get_html_theme_path

CONF = """
project = "Projeto Teste"
copyright = "2026, Teste"
html_theme = "{theme}"
html_theme_options = {{
    "primary_color": "#ff0066",
    "github_url": "https://github.com/org/repo",
    "footer_text": "Rodapé extra",
}}
"""


def build(tmp_path: Path) -> str:
    """Gera um projeto Sphinx mínimo com o tema e devolve o HTML da página inicial."""
    src = tmp_path / "src"
    src.mkdir()
    (src / "conf.py").write_text(CONF.format(theme=THEME_NAME), encoding="utf-8")
    (src / "index.rst").write_text("Título\n======\n\nTexto.\n", encoding="utf-8")
    out = tmp_path / "out"
    app = Sphinx(str(src), str(src), str(out), str(tmp_path / "doctrees"), "html", status=None, warningiserror=True)
    app.build()
    return (out / "index.html").read_text(encoding="utf-8")


def test_theme_path_contains_theme_toml() -> None:
    assert (Path(get_html_theme_path()) / "theme.toml").is_file()


def test_build_uses_theme_options(tmp_path: Path) -> None:
    html = build(tmp_path)
    assert "css/newtheme.css" in html
    assert "--nt-primary: #ff0066" in html
    assert 'href="https://github.com/org/repo"' in html
    assert "Rodapé extra" in html
    assert "data-nt-theme-toggle" in html


def test_static_files_are_copied(tmp_path: Path) -> None:
    build(tmp_path)
    static = tmp_path / "out" / "_static"
    assert (static / "css" / "newtheme.css").is_file()
    assert (static / "js" / "newtheme.js").is_file()
