#!/usr/bin/env python3
"""Copy a dossier's published page into the portal, wrapped in a full HTML document.

The dossier repositories render their page for an embedding viewer (no doctype, no ``<html>``,
``<head>`` or ``<body>``: the viewer adds them). On the portal the page is served as is, so this
script wraps the body in a standard skeleton (doctype, charset, viewport, canonical and sharing
metadata) and writes ``dossies/<pasta>/index.html``. The sha256 of the source page is printed and
recorded by ``make_provenance.py``. Usage: ``python3 sync_dossie.py <source.html> <pasta>``.
"""

import hashlib
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
DOSSIES = {
    "001-raio-x-do-brasil": {
        "titulo": "Raio-X do Brasil por governo",
        "descricao": "57 números de um infográfico viral conferidos contra fontes primárias sob uma regra fixada em código; 101 séries públicas com cadeia de hash desde 1964; índice pré-registrado de condições de vida; literatura revisada por pares por episódio; dívida externa nos dois conceitos do Banco Central.",
        "doi": "10.5281/zenodo.23604103",
    }
}


def embrulhar(corpo, pasta):
    """Return the full document for one dossier page body."""
    d = DOSSIES[pasta]
    url = f"https://brazilian.agency/dossies/{pasta}/"
    corpo = re.sub(r"<meta name=\"claude:[^>]*>\s*", "", corpo)
    cabeca = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="canonical" href="{url}">
<meta name="description" content="{d["descricao"]}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Open Source Brazilian Intelligence Agency">
<meta property="og:locale" content="pt_BR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{d["titulo"]} · Dossiê {pasta[:3]}">
<meta property="og:description" content="{d["descricao"]}">
<meta property="og:image" content="https://brazilian.agency/assets/emblema-gemini.png">
<meta name="twitter:card" content="summary">
<meta name="twitter:site" content="@ulissesflores">
<link rel="icon" href="/assets/emblema.svg" type="image/svg+xml">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Dataset","name":"{d["titulo"]}","url":"{url}","identifier":"https://doi.org/{d["doi"]}","sameAs":"https://doi.org/{d["doi"]}","license":"https://creativecommons.org/licenses/by/4.0/","isAccessibleForFree":true,"inLanguage":"pt-BR","creator":{{"@type":"Person","name":"Carlos Ulisses Flores","url":"https://orcid.org/0000-0002-6034-7765"}},"publisher":{{"@type":"Organization","name":"Open Source Brazilian Intelligence Agency","url":"https://brazilian.agency/"}}}}</script>
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}} body{{margin:0}} img{{max-width:100%}} [hidden]{{display:none!important}}</style>
</head>
<body>
"""
    return cabeca + corpo + "\n</body>\n</html>\n"


def main(argv):
    """Wrap ``argv[0]`` into ``dossies/argv[1]/index.html``; print the source hash; return 0."""
    fonte, pasta = Path(argv[0]), argv[1]
    corpo = fonte.read_text(encoding="utf-8")
    alvo = RAIZ / "dossies" / pasta / "index.html"
    alvo.parent.mkdir(parents=True, exist_ok=True)
    alvo.write_text(embrulhar(corpo, pasta), encoding="utf-8")
    print(
        f"{alvo.relative_to(RAIZ)} <- {fonte} sha256 {hashlib.sha256(fonte.read_bytes()).hexdigest()}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
