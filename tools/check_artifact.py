"""Verify packaged file hashes, Python syntax, and result arithmetic."""
from pathlib import Path
import ast, hashlib, json

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
for item in manifest["files"]:
    path = root / item["path"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"], str(path)
    if path.suffix == ".py":
        ast.parse(path.read_text(encoding="utf-8"))
for row in json.loads((root / "results/reference_counts.json").read_text(encoding="utf-8"))["shared_corpus"]:
    assert row["covered_successes"] <= row["covered_queries"] <= 2244
print("Verified", len(manifest["files"]), "file hashes and Python syntax. GPU experiments were not run.")
