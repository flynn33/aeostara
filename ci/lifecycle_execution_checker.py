#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from common_checks import print_result, repo_root_from_arg
from fixture_validator import FixtureSuiteEvaluator


class LifecycleExecutionChecker:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.evaluator = FixtureSuiteEvaluator(root)

    def validate(self) -> list[str]:
        failures: list[str] = []
        fixture_file = "end_to_end_healing_vectors.json"
        for run in range(2):
            run_failures = self.evaluator.evaluate_file(fixture_file)
            failures.extend(f"run {run + 1}: {failure}" for failure in run_failures)
        first_hash = self._actual_hash(fixture_file)
        second_hash = self._actual_hash(fixture_file)
        if first_hash != second_hash:
            failures.append("lifecycle actual output is not deterministic across two runs")
        return failures

    def _actual_hash(self, fixture_file: str) -> str:
        data = json.loads((self.root / "fixtures" / "conformance" / fixture_file).read_text(encoding="utf-8"))
        actual = [
            self.evaluator.evaluate_vector(fixture_file, vector).actual
            for vector in data.get("vectors", [])
        ]
        encoded = json.dumps(actual, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    root = repo_root_from_arg(sys.argv, __file__)
    failures = LifecycleExecutionChecker(root).validate()
    return print_result("lifecycle execution", failures, "PASS: lifecycle execution vectors are deterministic and complete.")


if __name__ == "__main__":
    raise SystemExit(main())
