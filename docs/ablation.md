# Controlled experiment implementation

## Common inputs and output schema

Load the frozen matched 160-query IDs, source/target mapping, saved clean backgrounds, model protocol, and condition definitions. Record `query_id`, `condition`, ordered background IDs, complete prompt token count, attack position, rendered prompt hash, response text, and success label. Save within-batch intact anchors separately.

Full experiment drivers and input bundles are not yet included. The portable [constructor](../src/constructor.py) exposes the fixed core and one Gemma request variant only; it does not implement every model's selected configuration.

## Position experiment

Use Vicuna, the first four saved clean ANCE documents in their original order, and 150-token greedy decoding. Insert the unchanged core at positions one through five. Verify equal complete prompt token counts for each query and regenerate clean responses with the same budget. This produces 800 attack contexts plus 160 clean baselines.

For cached-rank reconstruction, use the saved top-five hit indicator. Queries without a hit use their clean outcome. Moving retrieved attacks to position five must preserve the original hit set; forced inclusion changes exposure and must be a separate condition.

## Component neutralization

Use position five and change P (source prefix), B (title block), F (answer wording), or Z (final target slot). Replace P/B with deterministic benign words. Replace `Therefore, The relevant answer is Z.` with `Here, this record is named Z.` for F. Replace the final target slot with a generic noun phrase for Z. Keep query and background target mentions unchanged.

Match the complete prompt token count, not just the edited passage's word count. Check all 1,120 primary query/condition pairs and retain nine suffix tokens. Use within-batch intact controls to compute differences. Thirteen conditions yield 2,080 contexts; including anchors yields 2,560 sequences.

Keep deletion controls separate because they change input length. Full-title rescoring excludes aliases. Scoring the first 48 tokens of a saved 150-token response changes the output span; it is not a fresh generation with a shorter budget.

For interactions, preserve all four paired component cells per query. Compute differences of risk differences. Simultaneous intervals use the maximum absolute centered bootstrap error across the three declared interactions. Apply Holm correction to all twelve declared non-intact component comparisons.

## Added-request comparison

Use four saved ColBERTv2 backgrounds, position five, and 48-token greedy decoding for each generator. A is core alone; B adds a plain linked request; C adds a formatted direct request; D adds a formatted linked request. Phi D uses its frozen answer-key setting.

Add 10–11 deterministic neutral words to C to match D's complete prompt length. Validate all 640 model/query length checks and 640 duplicate references. D must remain byte-identical to its frozen enhanced document. The four primary D–C paired tests form one Holm family. B and D differ in prompt length, so their comparison is not a length-controlled formatting test.

For the fixed-request factorial, cross target mention/answer statement with no request, plain direct request, and the same direct request in message format. Match prompt token counts across the six conditions and retain all 20 declared primary comparisons in the correction family.

## Output verification

Reject mismatched query sets, prompt lengths, background order, or frozen-document hashes before aggregation. Preserve per-query gain/loss counts and each comparison's protocol rather than combining the 48-token and 150-token experiments.
