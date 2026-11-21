<!-- template:start -->
# template-sphinx-theme

Template de tema Sphinx distribuído como pacote Python: herda do tema `basic`, registra-se pelo entry point
`sphinx.html_themes` (basta `html_theme = "..."`), tem opções em `theme.toml`, modo claro/escuro, testes de build com
cobertura mínima de 100%, mypy estrito, documentação feita com o próprio tema no GitHub Pages e release por tag com
publicação no PyPI via Trusted Publishing.

## Como usar

1. **Use this template > Create a new repository** (ex.: `minhamarca-sphinx-theme`).
2. Clone e rode o inicializador (só biblioteca padrão do Python 3.10+):

   ```bash
   python template_init.py --name minhamarca --description "Tema Sphinx da Minha Marca."
   ```

   `--name` gera o pacote `minhamarca_sphinx_theme` (também o nome do tema) e o nome no PyPI
   `minhamarca-sphinx-theme`. Use `--dry-run` para conferir antes.
3. Desenvolva:

   ```bash
   python -m venv .venv && . .venv/bin/activate   # no Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   pre-commit install --install-hooks -t pre-commit -t pre-push
   sphinx-autobuild docs docs/_build/html   # opcional: pip install sphinx-autobuild
   ```

---
<!-- template:end -->
# newtheme-sphinx-theme

{{DESCRIPTION}}

[![QA](https://github.com/{{OWNER}}/newtheme-sphinx-theme/actions/workflows/qa.yml/badge.svg)](https://github.com/{{OWNER}}/newtheme-sphinx-theme/actions/workflows/qa.yml)

Documentação: <https://{{OWNER}}.github.io/newtheme-sphinx-theme/>

## Instalação

```bash
pip install newtheme-sphinx-theme
```

```python
# conf.py
html_theme = "newtheme_sphinx_theme"
html_theme_options = {
    "primary_color": "#1351b4",
    "github_url": "https://github.com/org/repo",
    "footer_text": "",
}
```

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `src/newtheme_sphinx_theme/__init__.py` | `setup()` que registra o tema e expõe a versão aos templates |
| `src/newtheme_sphinx_theme/theme.toml` | Herança (`basic`), CSS, barras laterais e opções |
| `src/newtheme_sphinx_theme/layout.html` | Cabeçalho, rodapé e opções aplicadas |
| `src/newtheme_sphinx_theme/static/` | CSS e JS (tema claro/escuro) |

## Desenvolvimento

```bash
pip install -e ".[dev]"
ruff check . && ruff format --check . && mypy && pytest
sphinx-build -W -b html docs docs/_build/html
```

## Release

1. Atualize `version` no `pyproject.toml` e a seção no `CHANGELOG.md`.
2. `git tag vX.Y.Z && git push origin vX.Y.Z`: o workflow `release.yml` confere a versão, cria a release e publica
   no PyPI.

## Licença

[MIT](LICENSE.md).
