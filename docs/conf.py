"""Configuração do Sphinx: a documentação usa o próprio tema."""

from __future__ import annotations

from importlib.metadata import version as package_version

project = "newtheme-sphinx-theme"
author = "{{AUTHOR}}"
copyright = "{{YEAR}}, {{AUTHOR}}"
release = package_version("newtheme-sphinx-theme")

extensions = ["sphinx.ext.githubpages"]
exclude_patterns = ["_build"]

html_theme = "newtheme_sphinx_theme"
html_title = f"newtheme-sphinx-theme {release}"
html_theme_options = {
    "github_url": "https://github.com/{{OWNER}}/newtheme-sphinx-theme",
}
