#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


class ProgramCloseoutRunner:
    def __init__(self, root: Path, online: bool) -> None:
        self.root = root
        self.online = online

    def run(self) -> int:
        failures = 0
        failures += self._run(["python3", "ci/conformance_runner.py", "."])
        failures += self._run(["python3", "ci/release_readiness_checker.py", "."])
        if self.online:
            failures += self._run(["python3", "ci/repository_separation_checker.py", ".", "--read-only", "--online"])
        if failures:
            print(f"FAIL: program closeout failed in {failures} command(s).")
            return 1
        print("PASS: program closeout suite passed.")
        return 0

    def _run(self, command: list[str]) -> int:
        result = subprocess.run(command, cwd=self.root, check=False)
        return 0 if result.returncode == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Aeostara final program closeout checks")
    parser.add_argument("repo_root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--online", action="store_true")
    args = parser.parse_args()
    return ProgramCloseoutRunner(Path(args.repo_root).resolve(), args.online).run()


if __name__ == "__main__":
    raise SystemExit(main())
