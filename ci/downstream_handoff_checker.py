#!/usr/bin/env python3
from __future__ import annotations

import sys
from common_checks import print_result, read_text, repo_root_from_arg

REQUIRED_HANDOFF = [
    "implementation_handoff/platform_repo_requirements.md",
    "implementation_handoff/required_contracts.md",
    "implementation_handoff/required_adapters.md",
    "implementation_handoff/required_conformance_artifacts.md",
    "implementation_handoff/windows_implementation_notes.md",
    "implementation_handoff/mac_implementation_notes.md",
    "implementation_handoff/ios_implementation_notes.md",
    "templates/platform_repo/README.template.md",
    "templates/platform_repo/conformance/module-mapping.template.md",
    "templates/platform_repo/conformance/verification-report.template.md",
    "templates/platform_repo/conformance/diagnostics-conformance.template.md",
    "templates/platform_repo/conformance/materialization-boundary.template.md",
    "templates/platform_repo/conformance/deviation-log.template.md",
    "templates/platform_repo/conformance/acceptance-judgment.template.md",
    "templates/platform_repo/ci/downstream-conformance.template.yml",
]


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures: list[str] = []
    for rel in REQUIRED_HANDOFF:
        if not (root / rel).is_file():
            failures.append(f"missing downstream handoff artifact: {rel}")
    combined = "\n".join(read_text(root / rel) for rel in REQUIRED_HANDOFF if (root / rel).is_file())
    for phrase in ["CONFORMANT", "CONFORMANT WITH CAVEATS", "NON-CONFORMANT", "deviation", "diagnostics", "module"]:
        if phrase.lower() not in combined.lower():
            failures.append(f"handoff artifacts missing phrase: {phrase}")
    for pattern in ["*.swift", "*.cpp", "*.h", "Package.swift"]:
        matches = [p for p in root.glob(f"**/{pattern}") if ".git" not in p.parts]
        if matches:
            failures.append(f"base repo contains native implementation source matching {pattern}: {matches[0].relative_to(root)}")
    return print_result("downstream handoff", failures, "PASS: downstream platform handoff package is present and base repo has no native implementation source.")


if __name__ == "__main__":
    raise SystemExit(main())
