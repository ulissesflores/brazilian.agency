#!/usr/bin/env python3
"""Seal the portal: one SHA-256 ``chain_hash`` over every published file, plus the dossier's origin.

``python3 make_provenance.py`` writes ``output/provenance.json`` and ``output/hash-chain.md``;
``python3 make_provenance.py --verify`` recomputes and compares. The dossier page is a copy of
``output/raio-x.html`` of the source repository; its sha256 and the source commit are recorded so a
reader can check that the copy is the sealed one.
"""

import hashlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
PUBLICADOS = ("index.html", "404.html", "robots.txt", "sitemap.xml", "CNAME", "sync_dossie.py")
PASTAS = ("assets", "dossies", "tests")
FONTE = {
    "repositorio": "https://github.com/ulissesflores/brazil-governments-factcheck",
    "doi": "10.5281/zenodo.23604103",
    "pagina_fonte": "output/raio-x.html",
    "sha256_fonte": "a5b5e9ebf77a32b52663226c6b7765006b8254c4fa2a69118352662e74b6440b",
}


def arquivos():
    """List the sealed files, relative to the repository root, sorted by path."""
    achados = {Path(p) for p in PUBLICADOS + ("make_provenance.py", "run_all.py")}
    for pasta in PASTAS:
        achados |= {
            p.relative_to(RAIZ)
            for p in (RAIZ / pasta).rglob("*")
            if p.is_file() and "__pycache__" not in p.parts
        }
    return sorted(achados, key=lambda p: p.as_posix())


def sha256(caminho):
    """Hex SHA-256 of a file."""
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def construir():
    """Compute the chain over the sealed files and return the provenance record."""
    h = hashlib.sha256(b"").hexdigest()
    itens = []
    for p in arquivos():
        d = sha256(RAIZ / p)
        h = hashlib.sha256((h + p.as_posix() + d).encode()).hexdigest()
        itens.append({"path": p.as_posix(), "sha256": d})
    dossie = RAIZ / "dossies" / "001-raio-x-do-brasil" / "index.html"
    return {
        "chain_hash": h,
        "files": itens,
        "dossie_001": {"sha256": sha256(dossie), **FONTE},
        "rule": "h_0 = sha256(''); h_i = sha256(h_{i-1} + path_i + sha256(file_i)); path order",
    }


def main(argv):
    """Write or verify the seal; return a process exit code."""
    novo = construir()
    alvo = RAIZ / "output" / "provenance.json"
    if "--verify" in argv:
        velho = json.loads(alvo.read_text(encoding="utf-8"))
        antigos = {f["path"]: f["sha256"] for f in velho["files"]}
        novos = {f["path"]: f["sha256"] for f in novo["files"]}
        for p in sorted(set(antigos) | set(novos)):
            if antigos.get(p) != novos.get(p):
                print(f"DIVERGES: {p}")
        if velho["chain_hash"] != novo["chain_hash"]:
            print("PROVENANCE FAILED")
            return 1
        print(f"provenance verified: chain_hash {novo['chain_hash']}")
        return 0
    alvo.parent.mkdir(exist_ok=True)
    alvo.write_text(json.dumps(novo, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    linhas = ["# Hash chain of the portal", "", f"`chain_hash` = `{novo['chain_hash']}`", ""]
    linhas += [f"- `{f['path']}` `{f['sha256'][:16]}`" for f in novo["files"]]
    (RAIZ / "output" / "hash-chain.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"chain_hash {novo['chain_hash']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
