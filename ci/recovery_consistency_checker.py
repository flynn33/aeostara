#!/usr/bin/env python3
from __future__ import annotations

import sys
from common_checks import load_json, print_result, read_text, repo_root_from_arg

REQUIRED_CATEGORIES = {"NO_ACTION", "NORMALIZE_STATE", "APPLY_CORRECTION", "FALLBACK_REQUIRED", "CONTAINMENT_REQUIRED", "ESCALATION_REQUIRED", "TERMINAL_NO_RECOVERY"}


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures: list[str] = []
    recovery_plan_doc = read_text(root / "specs" / "algorithms" / "recovery_plan_generation.pseudo.md")
    recovery_schema = read_text(root / "specs" / "contracts" / "RecoveryPlan.schema.json")
    if 'step("NO_OP"' in recovery_plan_doc:
        failures.append("recovery plan still emits an executable NO_OP step")
    if '"NO_OP"' in recovery_schema:
        failures.append("RecoveryPlan schema still allows NO_OP as a step or disposition")
    schema_text = read_text(root / "specs" / "contracts" / "RecoveryPlan.schema.json")
    for phrase in ["planDisposition", "recoverySteps", "RecoveryStep.schema.json"]:
        if phrase not in schema_text:
            failures.append(f"RecoveryPlan schema missing {phrase}")
    combined = "\n".join(read_text(root / "specs" / "algorithms" / name) for name in [
        "recovery_step_generation.pseudo.md",
        "recovery_blocked_path_escalation.pseudo.md",
        "policy_gate_lifecycle.pseudo.md",
        "backup_lifecycle.pseudo.md",
        "execution_step_lifecycle.pseudo.md",
        "verification_plan_generation.pseudo.md",
        "rollback_lifecycle.pseudo.md",
        "fallback_selection.pseudo.md",
        "containment_mode.pseudo.md",
        "safe_halt_semantics.pseudo.md",
    ])
    for phrase in ["monotonic", "Fallback", "Containment", "Safe Halt", "diagnostic", "audit"]:
        if phrase.lower() not in combined.lower():
            failures.append(f"recovery lifecycle docs missing phrase: {phrase}")
    observed_categories: set[str] = set()
    for name in ["recovery_escalation_vectors.json", "policy_block_vectors.json", "backup_rollback_vectors.json", "safe_halt_terminal_vectors.json"]:
        try:
            for vector in load_json(root / "fixtures" / "conformance" / name).get("vectors", []):
                expected = vector.get("expected", {})
                observed_categories.add(expected.get("recoveryCategory", ""))
        except Exception as exc:  # noqa: BLE001
            failures.append(f"cannot load {name}: {exc}")
    missing = REQUIRED_CATEGORIES - observed_categories
    for category in sorted(missing):
        failures.append(f"recovery fixtures missing category: {category}")
    return print_result("recovery consistency", failures, "PASS: recovery categories, NO_ACTION semantics, and escalation fixtures are consistent.")


if __name__ == "__main__":
    raise SystemExit(main())
