# ECHO

**Training-free RAG Poisoning via Fixed Templates and Coupled Requests**

Code and implementation instructions for studying targeted corpus poisoning against explicit user exclusions in retrieval-augmented generation (RAG).

ECHO constructs a document from relevant source text, repeated title words, and an answer statement, then adds a forged request. Retrieval determines whether the document reaches the generator. Source quarantine inspects retrieved documents and replenishes the context from saved candidates.

## Start here

```bash
git clone https://github.com/Affect1onate/ECHO.git
cd ECHO
python tools/check_artifact.py
python examples/inspect_sources.py
```

Both Python commands use only the standard library and require no model weights or GPU.

## What is included

| Component | Entry point | Status |
|---|---|---|
| Source quarantine | [Inspection and filtering](src/source_quarantine.py) | Original rule implementation |
| Fixed document construction | [Core and Gemma request](src/constructor.py) | Portable extraction; selected Gemma variant only |
| Integrity checks | [Artifact checker](tools/check_artifact.py) | SHA256 and syntax checks |
| Experiment instructions | [Reproduction guide](docs/reproduction.md) | Inputs, protocols, and release status |

**Release scope:** this initial package supports the examples and inspection checks above.

## Implementation and reproduction guides

- [Environment, inputs, and execution order](docs/reproduction.md)
- [Evaluation and baseline configuration](docs/evaluation.md)
- [Shared corpora, source access, and document processing](docs/corpus_checks.md)
- [Position, component, and request controls](docs/ablation.md)
- [Defense verification](docs/defense.md)
- [Artifact provenance and reuse](docs/research_practices.md)

The guides cover required inputs, configuration, execution order, output records, and verification checks. Scientific findings and discussion are in the paper.

## Reported full-query results

All rows evaluate 2,244 queries. Values are ASR (%), including retrieval misses.

| Pipeline | Strongest evaluated baseline | ECHO |
|---|---:|---:|
| E5-Mistral / Gemma | 18.54 | 90.51 |
| BM25 / Gemma | 19.12 | 87.70 |
| Contriever / Phi | 53.16 | 90.55 |
| ColBERTv2 / Vicuna | 74.69 | 78.97 |

The strongest baseline in these four comparisons is ChatInject. The maximum relative gain is 388.22%, calculated from unrounded success counts. These are isolated per-query injections; the shared-corpus experiment is documented separately.

## Data, models, and reuse

Model checkpoints and upstream datasets are not redistributed. Obtain them from their providers under the applicable licenses. No software license has been selected for this repository yet; public availability alone does not grant an open-source license. No acceptance, publication, or reproducibility badge is claimed.
