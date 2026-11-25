# Reproduction guide

## Commands available in this package

Run the commands in the repository README from the repository root. `tools/check_artifact.py` validates integrity and syntax. `examples/inspect_sources.py` checks a synthetic construction/filtering example. `scripts/plot_sample_size_scaling.py --output-dir figures` writes `sample_size_scaling_asr.png` and `.pdf` from measured aggregates embedded in the script.

## Inputs required for full experiments

Full inference is not runnable from this initial package alone. It requires the following versioned inputs in addition to upstream model weights:

| Input | Required fields or contents | Current package |
|---|---|---|
| Reconstructed corpus | 90,406 ordered source documents and stable identifiers | Not bundled |
| Query partition | 1,208 development / 2,244 test queries, paired source and excluded target | Not bundled |
| Query selections | Matched 160 IDs; separate nested order; disjoint development/control IDs | Not bundled |
| Frozen attacks | Exact document bytes and generator-specific selected requests | Not bundled |
| Retrieval records | Ordered candidates, scores, injected document identifiers | Not bundled |
| Model protocol | Checkpoint revision, prompt serialization, tokenizer, decoding settings | Described below; per-run manifests not bundled |
| Response records | Query ID, condition, rendered-prompt hash, response, success label, measured time | Not bundled |

Do not replace missing frozen inputs with newly selected examples and describe the result as an exact reproduction.

## Execution order for the full pipeline

1. Reconstruct and hash the corpus; verify source/target mappings and fixed query IDs.
2. Freeze constructors and per-generator request configuration before evaluation.
3. Save clean retrieval and generation records.
4. Inject documents under the specified isolated or shared-corpus protocol; rerun retrieval and save ordered contexts.
5. Generate responses under the frozen prompt and decoding settings; use the same success rule for every method.
6. Run paired controls, calculate query-level statistics, and verify denominators before plotting.

This is an execution specification, not a claim that the full drivers have already been released. Concrete full-run commands will accompany the corresponding drivers and data manifests.

## Recorded environment

The supplied experimental notes record RTX 5070 Ti, Python 3.11.15, PyTorch 2.11.0 / CUDA 12.8, and Transformers 5.19.0 for diagnostics. These are provenance values, not a tested universal installation recipe. Plot reconstruction was tested separately with the local Python/Matplotlib environment.

Main generation uses NF4 double quantization, bfloat16 computation, greedy decoding, one beam, and 48 output tokens. Gemma uses eager attention; the other original generators use SDPA. Position and fixed-core component diagnostics use 150 output tokens. Model repositories and data licenses remain governed by their providers.
