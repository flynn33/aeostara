#!/usr/bin/env python3
from __future__ import annotations

import sys
from common_checks import load_json, print_result, read_text, repo_root_from_arg


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures: list[str] = []
    projection_doc = read_text(root / "specs" / "algorithms" / "semantic_projection.pseudo.md")
    confidence_doc = read_text(root / "specs" / "algorithms" / "mapping_confidence_evaluation.pseudo.md")
    failure_doc = read_text(root / "specs" / "algorithms" / "mapping_failure_handling.pseudo.md")
    combined = projection_doc + confidence_doc + failure_doc
    for coord in [f"b{i}" for i in range(9)]:
        if coord not in projection_doc:
            failures.append(f"semantic projection missing coordinate {coord}")
    for keyword in ["AMBIGUOUS", "BLOCKED", "FAILED", "MappingResult", "DiagnosticEnvelope"]:
        if keyword not in combined:
            failures.append(f"semantic projection docs missing {keyword}")
    path = root / "fixtures" / "conformance" / "semantic_projection_vectors.json"
    try:
        vectors = load_json(path).get("vectors", [])
        categories = {v.get("category", "") for v in vectors}
        for required in ["all-9-coordinates-mapped", "ambiguous-coordinate", "blocked-mapping"]:
            if required not in categories:
                failures.append(f"semantic projection fixtures missing category: {required}")
    except Exception as exc:  # noqa: BLE001
        failures.append(f"cannot load semantic projection fixtures: {exc}")
    return print_result("semantic projection", failures, "PASS: semantic projection covers all 9 coordinates and blocked/ambiguous behavior.")


if __name__ == "__main__":
    raise SystemExit(main())
