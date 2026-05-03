#!/usr/bin/env python3
from __future__ import annotations

import sys
from common_checks import REQUIRED_ASH_BINDINGS, print_result, read_text, repo_root_from_arg

REQUIRED_AREAS = [
    "State space",
    "Canonical codeword set",
    "Codeword transformation",
    "State admissibility",
    "State-validity diagnostics",
    "System-state classification",
    "Recoverability",
    "Fallback policy registry",
    "Containment and safe halt",
    "Realm identity",
    "Transition registry",
    "Topology generator",
    "Axiom evaluator",
    "Generation and materialization",
    "Invariant categories",
]


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures: list[str] = []
    for rel in ["ASH_BASELINE_REFERENCE.md", "specs/acceptance/ash_source_traceability.md", "specs/acceptance/ash_authority_traceability_matrix.md"]:
        if not (root / rel).is_file():
            failures.append(f"missing traceability artifact: {rel}")
    baseline = read_text(root / "ASH_BASELINE_REFERENCE.md")
    for area in REQUIRED_AREAS:
        if area.lower() not in baseline.lower():
            failures.append(f"ASH baseline reference missing area: {area}")
    for name in REQUIRED_ASH_BINDINGS:
        path = root / "specs" / "ash_baseline" / name
        if not path.is_file():
            failures.append(f"missing ASH binding: specs/ash_baseline/{name}")
            continue
        text = read_text(path)
        for phrase in ["Upstream ASH Source", "Aeostara Binding Responsibility", "Downstream Platform Obligation", "Diagnostics and Audit Requirements", "Conformance Tests"]:
            if phrase not in text:
                failures.append(f"{path.relative_to(root)} missing section: {phrase}")
    return print_result("ASH traceability", failures, "PASS: ASH baseline traceability artifacts cover required source areas.")


if __name__ == "__main__":
    raise SystemExit(main())
