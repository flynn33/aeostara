#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CHECKS = [
    "base_design_completion_checker.py",
    "validate_schemas.py",
    "fixture_validator.py",
    "traceability_checker.py",
    "ash_invariant_checker.py",
    "semantic_projection_checker.py",
    "diagnostic_chain_checker.py",
    "json_semantics_checker.py",
    "recovery_consistency_checker.py",
    "downstream_handoff_checker.py",
    "compliance_checker.py",
    "branch_alignment_checker.py",
]


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    failures = 0
    for script in CHECKS:
        args = [sys.executable, str(Path(__file__).resolve().parent / script), str(root)]
        if script == "branch_alignment_checker.py":
            args.extend(["--profile", "main"])
        result = subprocess.run(args, check=False)
        if result.returncode != 0:
            failures += 1
    if failures:
        print(f"FAIL: base-design conformance failed in {failures} checker(s).")
        return 1
    print("PASS: full Aeostara base-design conformance suite passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
