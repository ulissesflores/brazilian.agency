# Reproducibility

The portal is static: what you see at https://brazilian.agency is exactly the content of this repository on `main`, served by GitHub Pages.

## Seal 1: the portal itself (any machine, no network)

`python3 run_all.py` runs the tests (every local link and asset exists; search and sharing metadata are consistent; the independence line is on the page; the sitemap, robots and CNAME match the site; the dossier page is the sealed copy) and then `python3 make_provenance.py --verify`, which recomputes one SHA-256 `chain_hash` over every published file and compares it with `output/provenance.json`.

## Seal 2: the dossiers (frozen copies of sealed pages)

Each dossier page under `dossies/` is a byte copy of the page published by the dossier's own repository, which carries the hash chain of the raw data, the pre-registration, the tests and the DOI. `output/provenance.json` records, per dossier, the sha256 of the copy, the source repository and the DOI. The copy is not rebuilt here; to reproduce the dossier itself, clone its repository and run its `run_all.py`.

| Dossier | Source | DOI |
|---|---|---|
| 001 Raio-X do Brasil por governo | https://github.com/ulissesflores/brazil-governments-factcheck | 10.5281/zenodo.23604103 |

## What cannot be re-run

Nothing in the portal depends on a live service. DNS and the TLS certificate are operated by Hostinger (DNS) and GitHub (Pages); a mismatch between the site and the repository means a deployment in progress, never a change of content.
