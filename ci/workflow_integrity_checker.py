#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

from common_checks import print_result, read_text, repo_root_from_arg


class WorkflowIntegrityChecker:
    def __init__(self, root: Path) -> None:
        self.root = root

    def validate(self) -> list[str]:
        failures: list[str] = []
        workflow_dir = self.root / ".github" / "workflows"
        if not workflow_dir.is_dir():
            return ["missing .github/workflows"]
        workflows = sorted(workflow_dir.glob("*.yml")) + sorted(workflow_dir.glob("*.yaml"))
        if not workflows:
            return ["no workflow files found"]
        combined = ""
        for path in workflows:
            text = read_text(path)
            combined += "\n" + text
            rel = path.relative_to(self.root)
            failures.extend(self._scan_failure_suppression(rel, text))
            failures.extend(self._scan_path_exemptions(rel, text))
        if "ci/conformance_runner.py" not in combined:
            failures.append("workflow set must run ci/conformance_runner.py")
        if "workflow_integrity_checker.py" not in combined and "workflow-integrity" not in combined.lower():
            failures.append("workflow set must include workflow-integrity validation")
        return failures

    def _scan_failure_suppression(self, rel: Path, text: str) -> list[str]:
        failures: list[str] = []
        if re.search(r"continue-on-error\s*:\s*true", text, re.IGNORECASE):
            failures.append(f"{rel}: continue-on-error is failure suppression")
        for pattern in [r"\|\|\s*true", r"(^|\n)\s*run:\s*exit\s+0\s*($|\n)", r"if:\s*always\(\)"]:
            if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                failures.append(f"{rel}: suppressed failure pattern matched: {pattern}")
        return failures

    def _scan_path_exemptions(self, rel: Path, text: str) -> list[str]:
        failures: list[str] = []
        if str(rel) not in text and re.search(r"paths-ignore\s*:", text):
            failures.append(f"{rel}: paths-ignore cannot exempt workflow integrity from its own changes")
        if re.search(r"platform/\*\*", text):
            failures.append(f"{rel}: broad platform branch glob remains active")
        return failures


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures = WorkflowIntegrityChecker(root).validate()
    return print_result("workflow integrity", failures, "PASS: workflow integrity checks passed.")


if __name__ == "__main__":
    raise SystemExit(main())
