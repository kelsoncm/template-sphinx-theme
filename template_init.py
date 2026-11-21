#!/usr/bin/env python3
"""Inicializa um repositório gerado a partir do template-sphinx-theme.

Troca o tema de exemplo (``newtheme_sphinx_theme`` / ``newtheme-sphinx-theme``) e os marcadores
({{OWNER}}, {{DESCRIPTION}}...), renomeia as pastas e, por fim, apaga este script.

Uso (na raiz do repositório recém-criado):

    python template_init.py                       # pergunta o que não conseguir deduzir
    python template_init.py --name minhamarca --description "Tema Sphinx da Minha Marca." --yes
    python template_init.py --dry-run             # mostra o que mudaria, sem alterar nada

Sem dependências externas: só a biblioteca padrão do Python 3.10+.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SELF = Path(__file__).resolve()
SKIP_DIRS = {".git", "node_modules", "vendor", ".venv", "venv", "__pycache__", "_build", "_site", "dist"}
TEMPLATE_BLOCK = re.compile(r"<!-- template:start -->.*?<!-- template:end -->\n*", re.S)
RST_UNDERLINE = re.compile(r"^([=\-~^\"'`#*+])\1+$")


def git(*args: str) -> str:
    """Executa um comando git na raiz e devolve a saída (vazia se o git falhar)."""
    try:
        result = subprocess.run(  # noqa: S603 - argumentos fixos, git do PATH do desenvolvedor
            ["git", *args],  # noqa: S607
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return ""
    return result.stdout.strip()


def remote_owner_repo() -> tuple[str, str]:
    """Deduz dono e nome do repositório pela URL do remoto ``origin``."""
    match = re.search(r"[:/]([^/:]+)/([^/]+?)(?:\.git)?/?$", git("remote", "get-url", "origin"))
    return (match.group(1), match.group(2)) if match else ("", "")


def ask(label: str, default: str, interactive: bool) -> str:
    """Pergunta um valor no terminal, usando o padrão quando não houver resposta."""
    if not interactive:
        return default
    answer = input(f"{label} [{default}]: ").strip() if default else input(f"{label}: ").strip()
    return answer or default


def iter_paths() -> list[Path]:
    """Lista arquivos e pastas do repositório, ignorando .git, dependências e saídas de build."""
    paths = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts) or path == SELF:
            continue
        paths.append(path)
    return paths


def fix_rst_underlines(text: str) -> str:
    """Ajusta o sublinhado dos títulos reStructuredText ao novo tamanho do título."""
    lines = text.split("\n")
    for i in range(1, len(lines)):
        title = lines[i - 1]
        if title.strip() and not RST_UNDERLINE.match(title) and RST_UNDERLINE.match(lines[i]):
            lines[i] = lines[i][0] * max(len(title), 3)
    return "\n".join(lines)


def apply(replacements: dict[str, str], dry_run: bool) -> None:
    """Troca os marcadores no conteúdo e nos nomes dos arquivos e pastas."""
    ordered = sorted(replacements.items(), key=lambda item: -len(item[0]))
    for path in iter_paths():
        if not path.is_file():
            continue
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            continue  # binário (imagens, fontes...)
        new = text
        for old, value in ordered:
            new = new.replace(old, value)
        new = TEMPLATE_BLOCK.sub("", new)
        if path.suffix == ".rst":
            new = fix_rst_underlines(new)
        if new != text:
            print(f"  editado:   {path.relative_to(ROOT).as_posix()}")
            if not dry_run:
                path.write_bytes(new.encode("utf-8"))
    for path in sorted(iter_paths(), key=lambda p: len(p.parts), reverse=True):
        name = path.name
        for old, value in ordered:
            name = name.replace(old, value)
        if name != path.name:
            print(f"  renomeado: {path.relative_to(ROOT).as_posix()} -> {name}")
            if not dry_run:
                path.rename(path.with_name(name))


def common_arguments(parser: argparse.ArgumentParser, owner: str) -> None:
    """Argumentos comuns a todos os templates."""
    parser.add_argument("--owner", default=owner, help="organização ou usuário do GitHub (padrão: remoto origin)")
    parser.add_argument("--author", default=git("config", "user.name"))
    parser.add_argument("--email", default=git("config", "user.email"))
    parser.add_argument("--yes", action="store_true", help="não pergunta nada; usa argumentos e padrões")
    parser.add_argument("--dry-run", action="store_true", help="só mostra o que mudaria")


def require(values: dict[str, str]) -> bool:
    """Confere se nenhum valor ficou vazio."""
    missing = [key for key, value in values.items() if not value]
    if missing:
        print(f"erro: informe {', '.join(missing)} (veja --help)", file=sys.stderr)
        return False
    return True


def finish(dry_run: bool, steps: list[str]) -> None:
    """Apaga este script e mostra os próximos passos."""
    if dry_run:
        return
    SELF.unlink()
    print("\nPronto. Próximos passos:")
    for number, step in enumerate(["Revise as mudanças com `git status` e `git diff`.", *steps], 1):
        print(f"  {number}. {step}")


NAME_RE = re.compile(r"^[a-z][a-z0-9_]*[a-z0-9]$")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    owner, repo = remote_owner_repo()
    guess = re.sub(r"[-_]sphinx[-_]theme$", "", repo).replace("-", "_").lower()

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--name",
        default=guess if NAME_RE.match(guess) else "",
        help="nome do tema sem o sufixo _sphinx_theme, ex.: minhamarca (padrão: nome do repositório)",
    )
    parser.add_argument("--description", default="", help="descrição curta do tema")
    common_arguments(parser, owner)
    args = parser.parse_args()

    interactive = not args.yes and sys.stdin.isatty()
    name = ask("Nome do tema (sem _sphinx_theme)", args.name, interactive).removesuffix("_sphinx_theme")
    if not NAME_RE.match(name):
        print(f"erro: nome inválido {name!r}; use letras minúsculas, números e _", file=sys.stderr)
        return 2
    values = {
        "{{OWNER}}": ask("Dono no GitHub", args.owner, interactive),
        "{{DESCRIPTION}}": ask("Descrição curta", args.description, interactive),
        "{{AUTHOR}}": ask("Autor", args.author, interactive),
        "you@example.com": ask("E-mail do autor", args.email, interactive),
        "{{YEAR}}": str(date.today().year),
    }
    if not require(values):
        return 2
    dist = f"{name.replace('_', '-')}-sphinx-theme"
    values["newtheme-sphinx-theme"] = dist
    values["newtheme"] = name
    # As chaves são mais longas que {{OWNER}} e por isso são trocadas antes dele (ver apply).
    if repo:
        values["{{OWNER}}/newtheme-sphinx-theme"] = f"{values['{{OWNER}}']}/{repo}"
        values["{{OWNER}}.github.io/newtheme-sphinx-theme/"] = f"{values['{{OWNER}}']}.github.io/{repo}/"

    print(f"Inicializando {dist} (tema {name}_sphinx_theme){' [dry-run]' if args.dry_run else ''}")
    apply(values, args.dry_run)
    finish(
        args.dry_run,
        [
            'Instale: pip install -e ".[dev]" && pre-commit install --install-hooks -t pre-commit -t pre-push',
            "Ative o GitHub Pages (Settings > Pages > Source: GitHub Actions).",
            "Configure o Trusted Publisher no PyPI (workflow release.yml, environment pypi).",
            "Faça o commit inicial.",
        ],
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
