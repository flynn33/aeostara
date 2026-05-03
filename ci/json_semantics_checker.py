#!/usr/bin/env python3
from __future__ import annotations

import sys
from common_checks import load_json, print_result, read_text, repo_root_from_arg


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures: list[str] = []
    combined = "\n".join(read_text(root / "specs" / "algorithms" / name) for name in [
        "json_pointer_operations.pseudo.md",
        "json_canonicalization.pseudo.md",
        "surface_difference_generation.pseudo.md",
        "mutation_precondition_check.pseudo.md",
        "json_path.pseudo.md",
    ])
    for phrase in ["JSON Pointer", "missing", "null", "array", "canonical", "precondition", "evidence only"]:
        if phrase.lower() not in combined.lower():
            failures.append(f"JSON semantics docs missing phrase: {phrase}")
    legacy = read_text(root / "specs" / "algorithms" / "json_path.pseudo.md")
    for forbidden in ["split(dotPath", "RETURN null"]:
        if forbidden in legacy:
            failures.append(f"legacy dot-path helper remains active: {forbidden}")
    try:
        vectors = load_json(root / "fixtures" / "conformance" / "json_semantics_vectors.json").get("vectors", [])
        categories = {v.get("category", "") for v in vectors}
        for category in ["missing-vs-null", "object-key-with-dot", "arrays", "canonicalization-stability", "precondition-failure"]:
            if category not in categories:
                failures.append(f"JSON semantics fixtures missing category: {category}")
    except Exception as exc:  # noqa: BLE001
        failures.append(f"cannot load JSON semantics fixtures: {exc}")
    return print_result("JSON semantics", failures, "PASS: JSON Pointer, missing/null, arrays, canonicalization, and mutation preconditions are covered.")


if __name__ == "__main__":
    raise SystemExit(main())
