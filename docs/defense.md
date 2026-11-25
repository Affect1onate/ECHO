# Source quarantine usage

## Run the portable example

```bash
python examples/inspect_sources.py
```

[source_quarantine.py](../src/source_quarantine.py) is copied byte-for-byte from the original rule module. `inspect_source(text)` returns matching rule types and spans in normalized inspection text. It decodes HTML twice, applies NFKC, and checks message boundaries, role labels, override/output instructions, and answer assertions.

Pass ordered `(document_id, text)` pairs to `filter_sources(candidates[:10], limit=5)`. The function does not impose the ten-candidate cap itself. It returns up to five unflagged original passages plus an audit for all supplied candidates. Inspection normalization does not rewrite retained evidence. If fewer than five pass, the result is shorter. This module performs no retrieval or generation.

## Full evaluation configuration

Use the matched 160 queries, saved ColBERTv2 top-ten candidates, four generators, and 48-token greedy decoding. Use the same frozen statement-linked attack across models; Phi therefore differs from its main answer-key configuration. Freeze the rules on the designated 32 disjoint development queries before evaluation.

For each query, save candidate IDs/order, rule matches, retained IDs/order, original retained text, rendered prompt hash, and generated response. Compare attacked and clean contexts at both the document-text and order levels. Count retained passages and positive-document exposure separately from attack success.

## Response reuse and replay checks

Reuse saved responses only when model, query, complete rendered prompt, and decoding settings match. On the designated 32 preselected evaluation queries, regenerate both defended and undefended responses. Compare success labels with the cached labels; byte-identical generated text is not required. The denominator is two responses per query. This subset belongs to the existing evaluation cohort.

Include retrieval misses in paired attack reduction. Use the four exact paired McNemar tests as one Holm family and preserve paired conditions during query bootstrap resampling. Full candidate/response bundles and GPU replay drivers are not included in this initial package.
