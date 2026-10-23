#!/usr/bin/env python3
"""Single entry point: tests, then the seal check. No network.

``python3 run_all.py`` runs the test suite (structure of the pages, links, metadata, the dossier's
hash) and verifies ``output/provenance.json``; it ends in ``run_all: OK`` or ``run_all: FAILED``.
"""

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent


def rodar(nome, cmd):
    """Run one step in the repository root and return its exit code."""
    print(f"=== {nome} ===", flush=True)
    return subprocess.run(cmd, cwd=RAIZ).returncode


def main():
    """Run the two steps; return 0 only if both pass."""
    codigos = [
        rodar("1/2 pytest", [sys.executable, "-m", "pytest"]),
        rodar("2/2 provenance", [sys.executable, "make_provenance.py", "--verify"]),
    ]
    ok = not any(codigos)
    print(f"run_all: {'OK' if ok else 'FAILED'} (codes {codigos})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
