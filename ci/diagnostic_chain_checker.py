#!/usr/bin/env python3
from __future__ import annotations

import sys
from common_checks import load_json, print_result, read_text, repo_root_from_arg


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures: list[str] = []
    for rel in [
        "specs/contracts/DiagnosticEnvelope.schema.json",
        "specs/contracts/DiagnosticReference.schema.json",
        "specs/contracts/DiagnosticChain.schema.json",
        "specs/contracts/RuleReference.schema.json",
        "specs/contracts/AuditChain.schema.json",
        "specs/algorithms/diagnostic_chain_integrity.pseudo.md",
        "specs/algorithms/rule_id_validation.pseudo.md",
        "specs/algorithms/audit_chain_lifecycle.pseudo.md",
        "specs/acceptance/diagnostic_chain_conformance.md",
    ]:
        if not (root / rel).is_file():
            failures.append(f"missing diagnostic chain artifact: {rel}")
    text = "\n".join(read_text(root / rel) for rel in [
        "specs/algorithms/diagnostic_chain_integrity.pseudo.md",
        "specs/acceptance/diagnostic_chain_conformance.md",
    ])
    for phrase in ["parent", "root", "rule", "audit", "diagnostic"]:
        if phrase not in text.lower():
            failures.append(f"diagnostic chain docs missing phrase: {phrase}")
    try:
        vectors = load_json(root / "fixtures" / "conformance" / "diagnostic_chain_vectors.json").get("vectors", [])
        negatives = "\n".join("\n".join(v.get("negativeAssertions", [])) for v in vectors)
        for expected in ["missing parent", "orphan diagnostic", "rule-free diagnostic"]:
            if expected not in negatives:
                failures.append(f"diagnostic fixtures missing negative assertion: {expected}")
    except Exception as exc:  # noqa: BLE001
        failures.append(f"cannot load diagnostic chain fixtures: {exc}")
    return print_result("diagnostic chain", failures, "PASS: diagnostic chain contracts, algorithms, and negative fixtures are present.")


if __name__ == "__main__":
    raise SystemExit(main())
