#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from common_checks import print_result, read_text

SOURCE_EXTENSIONS = {".h", ".hpp", ".cpp", ".c", ".cc", ".cxx", ".m", ".mm", ".swift"}
REQUIRED_FILES = [
    "README.md",
    "REMEDIATION_STATUS.md",
    "BASE_DESIGN_COMPLETION.md",
    "ASH_BASELINE_REFERENCE.md",
    "specs/architecture/ash_authority_and_aeostara_conformance.md",
    "specs/acceptance/base_design_completion_gates.md",
    "conformance/manifest.json",
]
DISALLOWED_PATTERNS = [
    re.compile(r"Aeostara core defines ASH semantics", re.IGNORECASE),
    re.compile(r"ASH subsystem of Aeostara", re.IGNORECASE),
    re.compile(r"generic diff engine.*ASH compliant", re.IGNORECASE),
    re.compile(r"Branch alignment remains part of conformance scope", re.IGNORECASE),
]


def run_downstream_conformance(root: Path) -> list[str]:
    failures: list[str] = []
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            failures.append(f"Missing required artifact: {rel}")
    readme = read_text(root / "README.md")
    for phrase in ["Aeostara is platform-agnostic", "Platform repos consume Aeostara", "ASH"]:
        if phrase.lower() not in readme.lower():
            failures.append(f"README missing required phrase: {phrase}")
    for rel in ["README.md", "REMEDIATION_STATUS.md", "specs/architecture", "specs/acceptance"]:
        path = root / rel
        files = [path] if path.is_file() else list(path.glob("*.md")) if path.is_dir() else []
        for file in files:
            text = read_text(file)
            for pattern in DISALLOWED_PATTERNS:
                if pattern.search(text):
                    failures.append(f"Disallowed authority language in {file.relative_to(root)}: {pattern.pattern}")
    return failures


def run_source_safety(root: Path) -> list[str]:
    failures: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts or ".github" in path.parts or "ci" in path.parts or "templates" in path.parts:
            continue
        if path.suffix.lower() in SOURCE_EXTENSIONS:
            failures.append(f"Native platform implementation source present in base repo: {path.relative_to(root)}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Aeostara base-design compliance checker")
    parser.add_argument("repo_root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--mode", choices=["all", "downstream-conformance", "source-safety"], default="all")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    failures: list[str] = []
    if args.mode in {"all", "downstream-conformance"}:
        failures.extend(run_downstream_conformance(root))
    if args.mode in {"all", "source-safety"}:
        failures.extend(run_source_safety(root))
    return print_result("compliance", failures, "PASS: base-design compliance checks passed.")


if __name__ == "__main__":
    raise SystemExit(main())
