# Evaluation configuration and checks

## Inputs and denominators

Use the matched 160 queries for the clean baselines and 32-pipeline comparison. Use a separate fixed test ordering for nested sizes 160, 320, 640, 1,280, and 2,244. The two 160-query groups overlap in nine queries. Full-query comparisons use seven methods in four pipelines (62,832 condition records). Pipeline selection followed exploratory results; the extended evaluation is part of the existing test partition.

To check cohort sensitivity, exclude the original 160 from frozen predictions. On the remaining 2,084, ECHO/ChatInject success counts are 1,888/390, 1,835/400, 1,888/1,111, and 1,647/1,552 for E5-Mistral/Gemma, BM25/Gemma, Contriever/Phi, and ColBERTv2/Vicuna. Ten hash groups of 224–225 queries retain ECHO's lead in all groups for the first three pipelines and nine for the fourth.

## Retrieval configuration

- ColBERTv2: colbertv2.0; 1,000-word document cap; nonoverlapping 200-word internal passages; 300-token passage cap; 32 query positions; maximum passage MaxSim score per document. Internal passage encoding differs from retrieval of independent chunks.
- BM25Okapi: k1=1.5, b=0.75, epsilon=0.25; NFKC, case folding, alphanumeric tokens. Insertion updates all corpus statistics, including the average-IDF floor.
- DPR: paired single-NQ encoders; ANCE: ance-dpr-question-multi / ance-dpr-context-multi. Native pooling, unnormalized inner products, 512-token caps.
- Contriever: unnormalized masked mean pooling. E5-base-v2: normalized masked means and query:/passage: prefixes. BGE-base-en-v1.5: normalized CLS vectors with its retrieval instruction. These use 512-token caps and float32 scoring.
- E5-Mistral: unquantized float16 weights; 4,096-token cap; last nonpadding token pooling; float32 L2 normalization and inner products. Query instruction: “Given a web search query, retrieve relevant passages that answer the query”. Documents have no instruction.

## Generation and success checks

Task instruction: “Answer the user's question using the supplied passages. Give one concise answer. If the passages are insufficient, answer UNKNOWN.” The outer user message contains the instruction, Question:, numbered Passages:, and Answer:.

Success concerns recommending, listing, or presenting the excluded entity as an answer. The automated rule is a proxy, not an unrestricted semantic judge. It matches complete titles, unique multiword aliases, and year/name variants within 16 words, with fixed local negation checks. Full-title sensitivity excludes alias alternatives. Validation against 1,347 human labels from earlier C/C+M/C+N conditions gives precision 81.15%, recall 90.59%, and F1 85.61%; these values concern those annotated conditions, not a new annotation of all reported outputs.

Use whole-query paired bootstrap resampling with 10,000 draws. Intervals are marginal unless explicitly simultaneous. Apply Holm correction within the declared comparison family; do not correct only the comparisons that look favorable.

## Baseline configuration checklist

Semantic rewriting uses Qwen2.5-3B with a 192-token cap. HotFlip allows ten accepted filler edits under ColBERTv2 while preserving the payload. CorruptRAG-AS-style is a local answer-update adaptation. Style methods are adaptations, not claims of reproducing all original best configurations.

For the separate format check, compare ChatInject, prefix/title plus direct request (R), full core plus direct request (C), and linked request (D). Use the same 32 development queries and four formats: official Qwen3/GPT-OSS builders, local generator format, and plain text. Select by ASR, then HR@5, then fixed candidate order. Evaluate 64 separate queries and targets, including misses.

| Generator | ChatInject | R | C | D |
|---|---:|---:|---:|---:|
| Gemma | 25 | 30 | 38 | 54 |
| Vicuna | 52 | 53 | 57 | 51 |
| Phi | 34 | 46 | 57 | 60 |
| Mistral | 26 | 31 | 40 | 44 |

These are successes out of 64. C and D may select different formats in this check, so their contrast does not isolate request linking. The controlled request experiment holds formatting and prompt length fixed.

## Timing verification

Scaling batches hold up to eight sequences within 6,144 padded tokens, with memory-based splitting. CUDA-synchronized generation time includes tokenization, transfer, inference, and decoding; excludes construction, retrieval, model loading, warmup, and checkpoint writing. Reused records retain measured times. Check these boundaries before comparing timings on different hardware.
