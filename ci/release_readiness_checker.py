#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import subprocess
import sys
from pathlib import Path

from build_release_package import ReleasePackageBuilder
from common_checks import print_result, repo_root_from_arg


REQUIRED_RELEASE_FILES = [
    "README.md",
    "LICENSE.md",
    "CHANGELOG.md",
    "BASE_DESIGN_COMPLETION.md",
    "ASH_BASELINE_REFERENCE.md",
    "aeostara-conformance-policy.json",
    "REPOSITORY_SEPARATION_STATUS.md",
    "REPOSITORY_MIGRATION_CLOSEOUT.md",
    "FINAL_CLOSEOUT_REPORT.md",
    "conformance/repository-separation-evidence.md",
    "ci/requirements.txt",
]


class ReleaseReadinessChecker:
    def __init__(self, root: Path) -> None:
        self.root = root

    def validate(self) -> list[str]:
        failures: list[str] = []
        for rel in REQUIRED_RELEASE_FILES:
            if not (self.root / rel).is_file():
                failures.append(f"missing release file: {rel}")
        failures.extend(self._check_contract_freeze())
        failures.extend(self._check_final_judgment())
        failures.extend(self._check_clean_tree())
        failures.extend(self._check_package_reproducibility())
        return failures

    def _check_contract_freeze(self) -> list[str]:
        failures: list[str] = []
        for path in sorted((self.root / "specs" / "contracts").glob("*.schema.json")):
            text = path.read_text(encoding="utf-8")
            if "TODO" in text or "TBD" in text:
                failures.append(f"contract file contains deferred marker: {path.relative_to(self.root)}")
        return failures

    def _check_final_judgment(self) -> list[str]:
        failures: list[str] = []
        for rel in [
            "FINAL_CLOSEOUT_REPORT.md",
            "REMEDIATION_STATUS.md",
            "REPOSITORY_MIGRATION_CLOSEOUT.md",
            "SELF_AUDIT_REPORT.md",
        ]:
            path = self.root / rel
            if path.is_file() and "Final judgment: `CONFORMANT`" not in path.read_text(encoding="utf-8"):
                failures.append(f"{rel} does not record final judgment `CONFORMANT`")
        return failures

    def _check_clean_tree(self) -> list[str]:
        status = subprocess.check_output(["git", "status", "--short"], cwd=self.root, text=True)
        if status.strip():
            return ["working tree is not clean"]
        return []

    def _check_package_reproducibility(self) -> list[str]:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_result = ReleasePackageBuilder(self.root, Path(first)).build()
            second_result = ReleasePackageBuilder(self.root, Path(second)).build()
            if first_result.sha256 != second_result.sha256:
                return ["release package SHA-256 differs across two builds"]
        return []


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures = ReleaseReadinessChecker(root).validate()
    return print_result("release readiness", failures, "PASS: release readiness checks passed.")


if __name__ == "__main__":
    raise SystemExit(main())
