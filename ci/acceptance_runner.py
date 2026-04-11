#!/usr/bin/env python3
"""
Aeostara Acceptance Artifact Runner
Validates acceptance-scenario coverage and traceability artifacts.
"""

import os
import sys
from typing import List


SCENARIO_KEYWORDS = [
    "semantically stable despite superficial drift",
    "semantically unstable despite minimal/no superficial drift",
    "correction blocked; fallback selected",
    "fallback unavailable; containment entered",
    "containment breach; safe halt entered",
    "verification failure triggers rollback/escalation",
    "policy gate blocks unsafe action before mutation",
]

REQUIRED_ACCEPTANCE_FILES = [
    "specs/acceptance/acceptance_targets.md",
    "specs/acceptance/remediation_acceptance_targets.md",
    "specs/acceptance/traceability_matrix.md",
    "specs/acceptance/ash_conformance_targets.md",
]

TRACEABILITY_KEYWORDS = [
    "StateValidityDiagnostic",
    "SystemStateClass",
    "RecoveryCategory",
    "RecoveryPlan",
    "FallbackDecision",
    "ContainmentDecision",
    "SafeHaltDecision",
]


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().lower()


def main() -> int:
    repo_root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    failures: List[str] = []

    loaded = {}
    for rel in REQUIRED_ACCEPTANCE_FILES:
        full = os.path.join(repo_root, rel)
        if not os.path.isfile(full):
            failures.append(f"Missing required acceptance artifact: {rel}")
            continue
        loaded[rel] = read_text(full)

    if failures:
        print("FAIL: acceptance artifact pre-check failed:")
        for issue in failures:
            print(f"  - {issue}")
        return 1

    targets = loaded["specs/acceptance/acceptance_targets.md"]
    for keyword in SCENARIO_KEYWORDS:
        if keyword not in targets:
            failures.append(f"Acceptance target missing scenario keyword: {keyword}")

    remediation = loaded["specs/acceptance/remediation_acceptance_targets.md"]
    for marker in ["Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4", "Scenario 5", "Scenario 6", "Scenario 7"]:
        if marker.lower() not in remediation:
            failures.append(f"Remediation targets missing marker: {marker}")

    traceability = loaded["specs/acceptance/traceability_matrix.md"]
    for keyword in TRACEABILITY_KEYWORDS:
        if keyword.lower() not in traceability:
            failures.append(f"Traceability matrix missing contract reference: {keyword}")

    if failures:
        print("FAIL: acceptance artifact validation failed:")
        for issue in failures:
            print(f"  - {issue}")
        return 1

    print("PASS: acceptance artifact validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
