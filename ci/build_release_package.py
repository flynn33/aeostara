#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


ARTIFACT_NAME = "aeostara-base-design-v1.0.0.zip"
INCLUDES = [
    "README.md",
    "LICENSE.md",
    "CHANGELOG.md",
    "BASE_DESIGN_COMPLETION.md",
    "ASH_BASELINE_REFERENCE.md",
    "aeostara-conformance-policy.json",
    "FINAL_CLOSEOUT_REPORT.md",
    "REPOSITORY_MIGRATION_CLOSEOUT.md",
    "REPOSITORY_SEPARATION_STATUS.md",
    "specs/ash_baseline/**",
    "specs/contracts/**",
    "specs/interfaces/**",
    "specs/algorithms/**",
    "specs/architecture/**",
    "specs/acceptance/**",
    "fixtures/conformance/**",
    "fixtures/schema_examples/**",
    "conformance/**",
    "implementation_handoff/**",
    "templates/platform_repo/**",
    "ci/**",
]
EXCLUDES = [
    ".git/**",
    "**/__pycache__/**",
    "**/*.pyc",
    "dist/**",
    "build/**",
    "_quarantine/**",
    "platform/**",
    "**/.DS_Store",
    "**/*.bundle",
]


@dataclass(frozen=True)
class PackageResult:
    artifact: Path
    checksum: Path
    sha256: str


class ReleasePackageBuilder:
    def __init__(self, root: Path, output_dir: Path) -> None:
        self.root = root
        self.output_dir = output_dir

    def build(self) -> PackageResult:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        artifact = self.output_dir / ARTIFACT_NAME
        files = self._selected_files()
        timestamp = self._zip_timestamp()
        with zipfile.ZipFile(artifact, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for rel in files:
                info = zipfile.ZipInfo(str(rel), timestamp)
                info.external_attr = 0o644 << 16
                archive.writestr(info, (self.root / rel).read_bytes())
        sha = hashlib.sha256(artifact.read_bytes()).hexdigest()
        checksum = self.output_dir / f"{ARTIFACT_NAME}.sha256"
        checksum.write_text(f"{sha}  {ARTIFACT_NAME}\n", encoding="utf-8")
        return PackageResult(artifact=artifact, checksum=checksum, sha256=sha)

    def _selected_files(self) -> list[Path]:
        selected: list[Path] = []
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(self.root)
            rel_posix = rel.as_posix()
            if self._matches(rel_posix, EXCLUDES):
                continue
            if self._matches(rel_posix, INCLUDES):
                selected.append(rel)
        return sorted(selected, key=lambda item: item.as_posix())

    def _matches(self, rel: str, patterns: list[str]) -> bool:
        return any(fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(f"./{rel}", pattern) for pattern in patterns)

    def _zip_timestamp(self) -> tuple[int, int, int, int, int, int]:
        try:
            raw = subprocess.check_output(["git", "show", "-s", "--format=%cI", "HEAD"], cwd=self.root, text=True).strip()
            date, time = raw.split("T", 1)
            year, month, day = [int(part) for part in date.split("-")]
            hour, minute, second = [int(part) for part in time[:8].split(":")]
            return (year, month, day, hour, minute, second)
        except Exception:
            return (2026, 6, 22, 0, 0, 0)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic Aeostara base-design release package")
    parser.add_argument("repo_root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--output-dir", default="dist")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    result = ReleasePackageBuilder(root, root / args.output_dir).build()
    print(f"PASS: built {result.artifact} sha256={result.sha256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
