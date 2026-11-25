# Source quarantine usage and verification

## Run the portable example

```bash
python examples/inspect_sources.py
```

`src/source_quarantine.py` is copied byte-for-byte from the original rule module. `inspect_source(text)` returns matching rule types and spans in normalized inspection text. It decodes HTML twice, normalizes NFKC, and detects message boundaries, role labels, override/output instructions, and answer assertions.

Pass ordered `(document_id, text)` pairs to `filter_sources(candidates[:10], limit=5)`. The function does not impose the ten-candidate cap itself. It returns up to five unflagged original passages and an audit for every supplied candidate. Inspection normalization does not rewrite retained evidence. If fewer than five pass, the list is shorter. No retrieval or generation is performed by this module.

## Full evaluation inputs

Use 160 matched queries, saved ColBERTv2 top-ten candidates, four generators, 48-token greedy decoding, and the same frozen statement-linked document across models. Phi therefore differs from its main answer-key setting. Rules are fixed on 32 disjoint development queries. Full candidate/response bundles are not included in this initial release.

| Generator | Undefended successes | Defended successes | Reduction (pp) | 95% bootstrap interval |
|---|---:|---:|---:|---|
| Gemma |136|8|80.00|[73.75,86.25]|
| Vicuna |127|55|45.00|[36.88,53.13]|
| Phi |79|18|38.13|[30.00,46.25]|
| Mistral |84|52|20.00|[11.88,28.13]|

Denominator: 160, including eight retrieval misses. Expected context checks: exposure 152→0; five retained documents for 160/160; defended contexts equal ordered clean contexts for 160/160; clean positive exposure 144→144; original documents flagged 0/90,406.

## Cache reuse and fresh replay

Reuse a response only if model, query, complete rendered prompt, and decoding settings match. On 32 preselected evaluation queries, fresh undefended/defended counts in the same model order are 26/1,22/11,18/3,18/9. Agreement with cached success labels is 64/64,62/64,62/64,61/64, counting two responses per query. This checks labels, not byte-identical response text, and uses a subset of the existing cohort.
