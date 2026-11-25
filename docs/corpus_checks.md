# Corpus and query run configuration

These instructions specify inputs and checks for the corpus/query experiments reported in the paper. Full drivers and frozen inputs are not yet bundled; they are not executable commands for this initial package.

## Shared document collection

1. Load the same 90,406-document clean corpus and the frozen pool of 2,244 attack documents.
2. Form nested insertion budgets of 160, 640, and 2,244 using the saved ordering. Index all documents at each budget together.
3. Evaluate all 2,244 queries at every budget using natural top-five contexts. Do not reuse isolated-injection ranks.
4. Record the query's designated target, its designated attack ID, all retrieved injected IDs, and the generated response.
5. Aggregate overall ASR over all queries and covered-query ASR over queries whose designated attack was inserted. Both denominators include retrieval misses. Track other injected targets separately; they do not automatically violate the current query's exclusion.

The published aggregate counts used for arithmetic checks are in [reference_counts.json](../results/reference_counts.json). They are reference outputs, not per-query evidence or a replacement for rerunning inference.

## Query rewritings

Use the saved 152 eligible query IDs and three checked rewritings per original query. Preserve the information need and excluded entity. Freeze each attack document across all its rewritings. Generate both clean and attacked responses. Store `original_query_id` alongside each rewritten query and resample by original query when computing paired uncertainty.

## Source access

Keep the victim corpus complete. Compare the paired source with the first eligible clean E5-Mistral result, optionally withholding all 160 paired positive passages from the attacker's source-selection pool. Save the pool definition, selected document ID, and source retrieval cost separately from document assembly cost.

## Chunking and preprocessing

Use BM25/Gemma on the matched 160 queries. Apply each operation uniformly to the clean corpus and injected documents. Preserve internal whitespace for chunking. For every query, insert all chunks of its single attack document together and recompute BM25 corpus statistics. Retrieve five chunks without merging parents.

Configuration grid: chunk sizes 64, 128, and 256 words, each with 0% or 25% overlap. Keep parent document IDs and chunk offsets to inspect duplicate-parent exposure. Run the clean condition under the same processing configuration.

Other processing configurations use two HTML decoding rounds followed by NFKC/whitespace normalization, exact normalized-document deduplication, compression of adjacent repeated token blocks of lengths 1–12, or removal of the specified message-boundary and standalone-role patterns. Preserve the exact patterns with the run configuration rather than substituting an arbitrary sanitizer.

Save retrieved chunk IDs, parent IDs, ranks, processing configuration, prompt hash, and success label. Verify BM25 insertion scoring against a small reference BM25Okapi case before a full run. Index rebuilding with unchanged data is an index-consistency check, not a longitudinal experiment.
