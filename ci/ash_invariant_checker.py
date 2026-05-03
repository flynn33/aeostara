#!/usr/bin/env python3
from __future__ import annotations

import sys
from common_checks import print_result, read_text, repo_root_from_arg

CATEGORIES = [
    "Algebraic/State Conformance",
    "Recovery/Fallback/Containment Conformance",
    "Diagnostics Conformance",
    "Generation/Materialization-Boundary Conformance",
    "Contract/Module Conformance",
]
FAMILIES = ["INV-STATE", "INV-ADMISSIBILITY", "INV-CODEWORD", "INV-RECOVERY", "INV-DIAG", "INV-AXIOM", "INV-PLAN", "INV-BOUNDARY", "INV-REALM", "INV-TRANS", "INV-TOPO"]


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures: list[str] = []
    combined = "\n".join([
        read_text(root / "specs" / "ash_baseline" / "invariant_coverage_map.md"),
        read_text(root / "conformance" / "invariant-coverage.md"),
        read_text(root / "specs" / "acceptance" / "ash_invariant_acceptance_matrix.md"),
    ])
    for category in CATEGORIES:
        if category.lower() not in combined.lower():
            failures.append(f"missing ASH conformance category: {category}")
    for family in FAMILIES:
        if family not in combined:
            failures.append(f"missing invariant family coverage: {family}")
    return print_result("ASH invariant coverage", failures, "PASS: all 5 ASH conformance categories and invariant families are covered.")


if __name__ == "__main__":
    raise SystemExit(main())
