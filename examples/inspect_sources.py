"""Synthetic local example: no network access or model inference."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.constructor import gemma_statement_record
from src.source_quarantine import filter_sources

source = "Delivery services\nThis record describes delivery service options."
attack = gemma_statement_record(source, "Example Supplier")
candidates = [("clean-1", "A neutral delivery record."), ("injected", attack)]
candidates += [("clean-" + str(i), "Neutral source number " + str(i)) for i in range(2, 10)]
retained, audit = filter_sources(candidates[:10], limit=5)
assert [docid for docid, _ in retained] == ["clean-1", "clean-2", "clean-3", "clean-4", "clean-5"]
assert next(row for row in audit if row["document_id"] == "injected")["quarantine"]
print("Retained:", ", ".join(docid for docid, _ in retained))
print("Synthetic example passed; this is not an ASR experiment.")
