#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from common_checks import print_result, read_text, repo_root_from_arg


ACTIVE_ALGORITHMS = [
    "json_canonicalization.pseudo.md",
    "json_pointer_operations.pseudo.md",
    "mutation_precondition_check.pseudo.md",
    "surface_difference_generation.pseudo.md",
    "state_normalization.pseudo.md",
    "semantic_projection.pseudo.md",
    "state_to_ash_mapping.pseudo.md",
    "mapping_confidence_evaluation.pseudo.md",
    "mapping_failure_handling.pseudo.md",
    "ash_diagnostic_evaluation.pseudo.md",
    "state_admissibility_binding.pseudo.md",
    "state_classification.pseudo.md",
    "recovery_category_selection.pseudo.md",
    "codeword_transformation_binding.pseudo.md",
    "realm_identity_binding.pseudo.md",
    "transition_registry_binding.pseudo.md",
    "topology_generation_binding.pseudo.md",
    "axiom_evaluation_binding.pseudo.md",
    "generation_materialization_boundary.pseudo.md",
    "recovery_step_generation.pseudo.md",
    "recovery_plan_generation.pseudo.md",
    "recovery_plan_deterministic_identity.pseudo.md",
    "recovery_blocked_path_escalation.pseudo.md",
    "fallback_selection.pseudo.md",
    "containment_mode.pseudo.md",
    "safe_halt_semantics.pseudo.md",
    "policy_gate_lifecycle.pseudo.md",
    "backup_lifecycle.pseudo.md",
    "execution_step_lifecycle.pseudo.md",
    "verification_plan_generation.pseudo.md",
    "execution_and_verification.pseudo.md",
    "rollback_lifecycle.pseudo.md",
    "diagnostic_chain_integrity.pseudo.md",
    "rule_id_validation.pseudo.md",
    "audit_chain_lifecycle.pseudo.md",
    "healing_flow.pseudo.md",
]

LEGACY_ALGORITHMS = {
    "json_path.pseudo.md": "json_pointer_operations.pseudo.md",
    "drift_analysis.pseudo.md": "surface_difference_generation.pseudo.md",
    "repair_planning.pseudo.md": "recovery_plan_generation.pseudo.md",
    "policy_evaluation.pseudo.md": "policy_gate_lifecycle.pseudo.md",
    "backup.pseudo.md": "backup_lifecycle.pseudo.md",
    "audit.pseudo.md": "audit_chain_lifecycle.pseudo.md",
    "rollback.pseudo.md": "rollback_lifecycle.pseudo.md",
    "verification.pseudo.md": "verification_plan_generation.pseudo.md",
}

REQUIRED_SECTIONS = [
    "Purpose and Authority Source",
    "Inputs and Outputs",
    "Preconditions",
    "Deterministic Ordering and Tie-Breaking",
    "Complete Pseudocode",
    "Outcomes",
    "DiagnosticEnvelope and Chain Linkage",
    "AuditEvent Ordering",
    "Side-Effect Classification",
    "Postconditions",
    "Negative Cases",
    "Fixture References",
    "Downstream Implementation Obligations",
]


class AlgorithmCompletenessChecker:
    def __init__(self, root: Path) -> None:
        self.root = root

    def validate(self) -> list[str]:
        failures: list[str] = []
        algorithm_dir = self.root / "specs" / "algorithms"
        for filename in ACTIVE_ALGORITHMS:
            text = read_text(algorithm_dir / filename)
            if not text:
                failures.append(f"missing active algorithm: specs/algorithms/{filename}")
                continue
            for section in REQUIRED_SECTIONS:
                if f"## {section}" not in text:
                    failures.append(f"{filename}: missing section {section}")
            for required in ["BLOCKED", "FAILED", "DiagnosticEnvelope", "AuditEvent"]:
                if required not in text:
                    failures.append(f"{filename}: missing required outcome term {required}")
            for forbidden in ["TODO", "TBD", "not implemented", "placeholder"]:
                if forbidden.lower() in text.lower():
                    failures.append(f"{filename}: contains forbidden marker {forbidden}")
        for filename, replacement in LEGACY_ALGORITHMS.items():
            text = read_text(algorithm_dir / filename)
            if "## Superseded Algorithm Notice" not in text or replacement not in text:
                failures.append(f"{filename}: must be an explicit supersession notice naming {replacement}")
        return failures


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures = AlgorithmCompletenessChecker(root).validate()
    return print_result("algorithm completeness", failures, "PASS: active algorithms are deterministic and complete.")


if __name__ == "__main__":
    raise SystemExit(main())
