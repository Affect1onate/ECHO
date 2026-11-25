# Corpus and query experiment recipes

## Source access

Inputs: matched 160 queries, complete victim corpus, source-selection pool, frozen generator settings. Compare the paired source, first clean E5-Mistral result without relevance labels, and first eligible result after withholding all 160 paired positives from the attacker's source pool. The victim corpus stays complete. Source selection adds one retrieval call outside document assembly.

Expected attack top-five hits / Gemma successes: paired source 158/143; retrieval-selected source 159/132; all paired positives withheld 155/131. Clean excluded responses: 7/160. These are reported reference counts.

## Query rewriting

Select 152 queries with clear information needs and exclusions, check three rewritings per query before attack evaluation, and freeze attack documents. Preserve the excluded entity and information need. Group uncertainty calculations by original query.

Expected E5-Mistral/Gemma counts: original 136/152; rewritings 395/456; clean rewritings 31/456. A separate target-unspecified universal document reaches top five on 0/160 queries. This control does not establish reuse against unknown targets.

## Shared corpus

Add nested pools of 160, 640, and 2,244 frozen documents to the same 90,406-document corpus; evaluate all 2,244 queries at each budget with natural top-five contexts. Do not reuse isolated-injection ranks for this experiment.

| Inserted documents | Overall ASR (%) | Successes / queries with designated document inserted |
|---|---:|---:|
| 160 | 14.75 | 141/160 |
| 640 | 31.19 | 556/640 |
| 2,244 | 82.62 | 1,854/2,244 |

Clean ETR is 8.73%. The covered-query denominators include retrieval misses. At the largest budget the designated attack reaches top five for 2,210 queries. Among 253 contexts containing different injected targets, responses return the designated target in 60 cases, another visible injected target in 158, and neither in 35. Count only the query's designated target toward ASR.

## Chunking and preprocessing

Use BM25/Gemma and 160 matched queries. Apply each operation uniformly to clean and injected documents. Insert all chunks of a single attack document together; recalculate BM25 statistics. Retrieve five chunks without parent merging. Preserve internal whitespace when chunking.

| Words/chunk | Overlap | ASR (%) | Clean ETR (%) |
|---|---:|---:|---:|
| 64 | 0% | 72.50 | 5.63 |
| 64 | 25% | 58.13 | 5.63 |
| 128 | 0% | 85.00 | 6.25 |
| 128 | 25% | 84.38 | 6.88 |
| 256 | 0% | 84.38 | 6.88 |
| 256 | 25% | 84.38 | 6.88 |

All six gains survive Holm correction across eleven conditions. Whole-document reference ASR/ETR is 83.75/6.88. Two HTML decoding rounds, NFKC, and whitespace normalization preserve these values. Exact normalized-document deduplication removes no documents. Compression of adjacent repeated token blocks (lengths 1–12) gives 82.50/7.50. Removing specified chat boundaries and standalone role labels gives 8.75/6.88, without significant gain. All four processing checks retain 152 attack hits. Rebuilding the unchanged BM25 index reproduces 160/160 hit decisions; this is a static consistency check, not a longitudinal deployment test.

Inspect both clean and attacked results: overlapping chunks can occupy several positions, changing clean evidence even before injection. Reference BM25Okapi agreement on small multi-insertion cases is within 1e-10.
