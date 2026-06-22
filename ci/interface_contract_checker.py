#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from common_checks import print_result, read_text, repo_root_from_arg


REQUIRED_SECTIONS = [
    "Single Responsibility",
    "Consumed Contract Types",
    "Produced Contract Types",
    "Operations",
    "Preconditions",
    "Postconditions",
    "Side-Effect Classification",
    "Determinism Requirements",
    "DiagnosticEnvelope and DiagnosticChain Obligations",
    "AuditEvent and AuditChain Obligations",
    "Blocked and Failure Behavior",
    "Downstream Swift Protocol Mapping Rule",
    "Downstream C++ Pure-Virtual Mapping Rule",
    "Verification Cases",
    "Prohibited Behavior",
]

REQUIRED_OPERATIONS = {
    "IHealingEngine.pseudo.md": ["dryRun", "heal"],
    "IPlatformObservationAdapter.pseudo.md": ["observe"],
    "IConfigAdapter.pseudo.md": [
        "canonicalize",
        "resolvePointer",
        "generateSurfaceDifferences",
        "validateMutationPreconditions",
    ],
    "ISemanticProjector.pseudo.md": ["project"],
    "IAshBindingProvider.pseudo.md": [
        "evaluateAdmissibility",
        "diagnoseState",
        "classifyState",
        "applyCodewordTransformation",
        "resolveRealmIdentity",
        "resolveTransition",
        "generateTopology",
        "evaluateAxioms",
        "generateMaterializationPlan",
        "planArtifactEmission",
    ],
    "IPolicyGate.pseudo.md": ["evaluate"],
    "IBackupProvider.pseudo.md": ["prepareBackup", "executeRollback"],
    "IExecutionAdapter.pseudo.md": ["executeStep"],
    "IPlatformMutationAdapter.pseudo.md": ["applyMutation"],
    "IVerificationAdapter.pseudo.md": ["verify"],
    "IAuditSink.pseudo.md": ["appendEvent", "persistChain", "readChain"],
    "IFileSystem.pseudo.md": ["read", "writeAtomically", "appendAtomically", "copyAtomically", "exists", "computeSHA256"],
}


class InterfaceContractChecker:
    def __init__(self, root: Path) -> None:
        self.root = root

    def validate(self) -> list[str]:
        failures: list[str] = []
        interface_dir = self.root / "specs" / "interfaces"
        for filename, operations in REQUIRED_OPERATIONS.items():
            path = interface_dir / filename
            text = read_text(path)
            if not text:
                failures.append(f"missing interface file: specs/interfaces/{filename}")
                continue
            for section in REQUIRED_SECTIONS:
                if f"## {section}" not in text:
                    failures.append(f"{filename}: missing section {section}")
            for operation in operations:
                if f"{operation}(" not in text:
                    failures.append(f"{filename}: missing operation {operation}")
            for forbidden in ["TODO", "TBD", "not implemented", "placeholder"]:
                if forbidden.lower() in text.lower():
                    failures.append(f"{filename}: contains forbidden placeholder marker {forbidden}")
        return failures


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures = InterfaceContractChecker(root).validate()
    return print_result("interface contract validation", failures, "PASS: interface contracts are implementation-ready.")


if __name__ == "__main__":
    raise SystemExit(main())
