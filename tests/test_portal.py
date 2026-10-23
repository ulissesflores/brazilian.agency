"""The portal's contract: valid pages, honest metadata, working links, the dossier as sealed."""

import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
INDEX = (RAIZ / "index.html").read_text(encoding="utf-8")


class _Coletor(HTMLParser):
    """Collect hrefs, srcs and the JSON-LD block of a page."""

    def __init__(self):
        super().__init__()
        self.links, self.scripts, self._ld = [], [], False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("a", "link") and a.get("href"):
            self.links.append(a["href"])
        if tag in ("img", "script") and a.get("src"):
            self.links.append(a["src"])
        self._ld = tag == "script" and a.get("type") == "application/ld+json"

    def handle_data(self, data):
        if self._ld:
            self.scripts.append(data)


def _coleta(texto):
    c = _Coletor()
    c.feed(texto)
    return c


def test_every_local_link_and_asset_exists():
    c = _coleta(INDEX)
    locais = [h.split("#")[0] for h in c.links if not h.startswith(("http", "#", "mailto"))]
    for h in locais:
        p = RAIZ / h.rstrip("/")
        assert p.exists() or (p / "index.html").exists(), h


def test_metadata_for_search_and_sharing_is_present_and_consistent():
    for trecho in (
        '<link rel="canonical" href="https://brazilian.agency/">',
        'property="og:image" content="https://brazilian.agency/assets/emblema-gemini.png"',
        'name="description"',
        '<html lang="pt-BR">',
    ):
        assert trecho in INDEX, trecho
    c = _coleta(INDEX)
    ld = json.loads(c.scripts[0])
    tipos = {n["@type"] for n in ld["@graph"]}
    assert {"Organization", "WebSite", "Dataset"} <= tipos
    dataset = next(n for n in ld["@graph"] if n["@type"] == "Dataset")
    assert dataset["identifier"] == "https://doi.org/10.5281/zenodo.23604103"


def test_independence_is_stated_on_the_page_and_no_state_symbol_is_claimed():
    assert "sem vínculo com" in INDEX and "Open Source" in INDEX
    assert "ABIN" not in INDEX.replace(
        "Agência Brasileira de Inteligência", ""
    )  # named only to deny the link
    assert "classified" not in INDEX.lower()


def test_sitemap_robots_and_cname_match_the_site():
    sitemap = (RAIZ / "sitemap.xml").read_text(encoding="utf-8")
    for loc in re.findall(r"<loc>(.*?)</loc>", sitemap):
        rel = loc.replace("https://brazilian.agency/", "")
        p = RAIZ / rel
        assert (p / "index.html").exists() if rel else (RAIZ / "index.html").exists(), loc
    assert "Sitemap: https://brazilian.agency/sitemap.xml" in (RAIZ / "robots.txt").read_text()
    assert (RAIZ / "CNAME").read_text().strip() == "brazilian.agency"


def test_dossier_001_is_the_sealed_copy():
    prov = json.loads((RAIZ / "output" / "provenance.json").read_text(encoding="utf-8"))
    pagina = RAIZ / "dossies" / "001-raio-x-do-brasil" / "index.html"
    assert hashlib.sha256(pagina.read_bytes()).hexdigest() == prov["dossie_001"]["sha256"]
    assert prov["dossie_001"]["doi"] == "10.5281/zenodo.23604103"
    texto = pagina.read_text(encoding="utf-8")
    assert texto.startswith("<!doctype html>") and "<title>Raio-X do Brasil</title>" in texto[:6000]
    assert (
        '<link rel="canonical" href="https://brazilian.agency/dossies/001-raio-x-do-brasil/">'
        in texto
    )
    assert "claude:viewport" not in texto
