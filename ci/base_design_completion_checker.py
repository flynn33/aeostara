#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from common_checks import print_result, read_text, repo_root_from_arg

REQUIRED_FILES = [
    "README.md",
    "REMEDIATION_STATUS.md",
    "BASE_DESIGN_COMPLETION.md",
    "ASH_BASELINE_REFERENCE.md",
    "specs/architecture/repository_role_contract.md",
    "specs/architecture/downstream_platform_repository_contract.md",
    "specs/architecture/platform_implementation_boundary.md",
    "specs/architecture/base_to_platform_versioning.md",
]
FORBIDDEN_ACTIVE_PATTERNS = [
    r"Branch alignment remains part of conformance scope",
    r"Branch alignment is enforced through profile contracts",
    r"platform branches implement native mechanics",
    r"required_any_globs.*swift",
    r"required_any_globs.*cpp",
]
REQUIRED_FRAGMENTS = [
    "Aeostara is platform-agnostic",
    "platform repos",
    "ASH",
    "does not depend on platform",
]


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures: list[str] = []
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            failures.append(f"missing base-design file: {rel}")
    authority_text = "\n".join(read_text(root / rel) for rel in ["README.md", "REMEDIATION_STATUS.md", "BASE_DESIGN_COMPLETION.md"])
    for fragment in REQUIRED_FRAGMENTS:
        if fragment.lower() not in authority_text.lower():
            failures.append(f"authority docs missing fragment: {fragment}")
    scan_text = "\n".join(
        read_text(path) for path in [root / "README.md", root / "REMEDIATION_STATUS.md", root / "PLATFORM_STATUS_MATRIX.md"]
    )
    scan_text += "\n" + "\n".join(read_text(path) for path in (root / "specs" / "architecture").glob("*.md"))
    scan_text += "\n" + "\n".join(read_text(path) for path in (root / "branch_profiles").glob("*.json"))
    for pattern in FORBIDDEN_ACTIVE_PATTERNS:
        if re.search(pattern, scan_text, re.IGNORECASE | re.DOTALL):
            failures.append(f"forbidden active platform/branch language remains: {pattern}")
    workflow_text = "\n".join(read_text(path) for path in (root / ".github" / "workflows").glob("*.yml"))
    for phrase in ["platform/windows", "platform/macos", "platform/ios", "platform/**"]:
        if phrase in workflow_text:
            failures.append(f"workflow still treats platform branch as active base gate: {phrase}")
    return print_result("base design completion", failures, "PASS: base-design role, authority, and dependency direction are consistent.")


if __name__ == "__main__":
    raise SystemExit(main())
