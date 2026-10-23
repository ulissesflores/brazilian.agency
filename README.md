<div align="center">

# Open Source Brazilian Intelligence Agency

**Inteligência de fontes abertas sobre política e dados do Brasil: dossiês com dado público hasheado, regra escrita antes do resultado, literatura revisada por pares e DOI. Projeto independente, sem vínculo com governo ou órgão público.**

![license: Apache-2.0 + CC BY 4.0](https://img.shields.io/badge/license-Apache--2.0%20%2B%20CC%20BY%204.0-blue)
![python](https://img.shields.io/badge/python-3.11%20%7C%203.12-informational)
![reproducible](https://img.shields.io/badge/sealed-SHA--256_chain-success)

[brazilian.agency](https://brazilian.agency) · [Dossiê 001](https://brazilian.agency/dossies/001-raio-x-do-brasil/) · [Repositório do dossiê](https://github.com/ulissesflores/brazil-governments-factcheck)

</div>

> [!IMPORTANT]
> **O que é.** O portal estático da Open Source Brazilian Intelligence Agency. "Open source" tem o sentido técnico: inteligência de fontes abertas (OSINT), código e dados abertos. Não é agência de governo, não tem relação com a Agência Brasileira de Inteligência nem com qualquer órgão público, e não guarda nada que não esteja publicado com a fonte.

> [!NOTE]
> Este repositório contém só o portal. Cada dossiê vive no seu próprio repositório, com cadeia de hash, pré-registro, testes e DOI; o portal copia a página publicada e registra o hash da cópia e a origem.

## O que este repositório contribui

1. **Um portal estático, sem CMS e sem banco**, servido pelo GitHub Pages com o domínio `brazilian.agency`: página inicial, dossiês, metadados para busca e compartilhamento (canonical, Open Graph, JSON-LD de Organization, WebSite e Dataset), sitemap e robots.
2. **Um selo**: `make_provenance.py` encadeia o SHA-256 de todo arquivo publicado num único `chain_hash` e registra, para cada dossiê, o hash da página copiada, o repositório de origem e o DOI.
3. **Testes que fecham o contrato editorial**: links e ativos existem, metadados são consistentes, a independência está declarada em toda página, o dossiê é a cópia selada.

## Em resumo

| Item | Valor |
|---|---|
| Dossiês publicados | 1 (Raio-X do Brasil por governo, DOI 10.5281/zenodo.23604103) |
| Hospedagem | GitHub Pages, domínio `brazilian.agency` (DNS na Hostinger) |
| Dependências de execução | nenhuma (Python padrão); testes com pytest |

## Início rápido

```bash
git clone https://github.com/ulissesflores/brazilian.agency && cd brazilian.agency
python3 run_all.py
```

Saída esperada termina com:

```text
provenance verified: chain_hash <64 hex>
run_all: OK (codes [0, 0])
```

## Atualizar um dossiê

Rode `python3 sync_dossie.py <pagina-publicada.html> <numero>-<slug>` (embrulha a página num documento HTML completo com metadados), depois `python3 make_provenance.py` (grava o hash novo e a origem em `output/provenance.json`), depois `python3 run_all.py`. O commit registra a versão do dossiê que entrou.

## O que se afirma e o que não se afirma

| Afirmado | Não afirmado | Congelado |
|---|---|---|
| Cada arquivo publicado está no selo e cada dossiê é a cópia hasheada de uma versão com DOI | Que o portal tenha qualquer autoridade além da fonte citada em cada número | A página de cada dossiê, até a próxima versão do seu repositório |
| A independência do projeto está escrita em toda página | Qualquer nota de mérito a governo ou pessoa | O emblema (coruja sobre o Cruzeiro do Sul, anel de elos), desenhado para este projeto |

## Integridade

```bash
python3 make_provenance.py --verify
```

recompõe o `chain_hash` de todos os arquivos publicados e confere o hash do dossiê contra `output/provenance.json`.

## Estrutura

```text
index.html                 página inicial (portal)
dossies/<n>-<slug>/        cópia selada da página de cada dossiê
assets/                    CSS, emblema em SVG (código) e em PNG (cabeçalho e redes)
robots.txt sitemap.xml     busca
404.html CNAME             GitHub Pages
make_provenance.py         selo; run_all.py: testes + selo; tests/
output/                    provenance.json, hash-chain.md
```

## Autor

Carlos Ulisses Flores. ORCID [0000-0002-6034-7765](https://orcid.org/0000-0002-6034-7765) · [ulissesflores.com](https://ulissesflores.com) · [Lattes](http://lattes.cnpq.br/6905246706890561)

## Citação

Cite o dossiê, não o portal: cada dossiê tem o próprio DOI (o 001 é 10.5281/zenodo.23604103). Metadados do portal em `CITATION.cff` e `codemeta.json`.

## Licença

Código: Apache-2.0. Textos, emblema e dados derivados: CC BY 4.0 (`LICENSES/`, `NOTICE`). As páginas de dossiê seguem a licença do repositório de origem.
