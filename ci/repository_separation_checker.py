#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

from common_checks import print_result, repo_root_from_arg


SOURCE_REPOSITORY = "flynn33/aeostara"
ASH_BASELINE_COMMIT = "e123f5d7fdbb381179971f721a3292c31eb1cbc2"
REQUIRED_RELEASE_TAG = "v1.0.0"
FINAL_BASE_PIN_FILE = "AEOSTARA_BASELINE_REFERENCE.md"

SOURCE_BRANCHES = {
    "platform/windows": {
        "destination_repo": "flynn33/Aeostara-Windows",
        "destination_branch": "main",
        "source_head": "0b5072181eb0576ba94018b5d7f945309bf2b8e5",
        "source_tree": "eca549814828de3eeb75ef7464b83a182ebd02f6",
        "commit_count": 13,
        "archive_tag": "archive/platform-windows-0b50721",
        "import_tag": "import/platform-windows-0b50721",
        "bundle": "/Volumes/NVME/GitHub/Aeostara-closeout-evidence/bundles/aeostara-platform-windows-0b50721.bundle",
        "bundle_sha256": "de43e37717bb5eef6493018fcdd0b34e92ea534e14c9b8962d31d013f0fff8e9",
        "required_workflows": {
            ".github/workflows/windows-build.yml",
            ".github/workflows/downstream-conformance.yml",
            ".github/workflows/workflow-integrity.yml",
            ".github/workflows/attribution-integrity.yml",
        },
    },
    "platform/macos": {
        "destination_repo": "flynn33/Aeostara-Mac-iOS",
        "destination_branch": "platform/macos",
        "source_head": "b992a4b7f7b0847744a86bc50e4b946b1ef84119",
        "source_tree": "edcd2e4c6edad9450bcec1db563540242e42c717",
        "commit_count": 17,
        "archive_tag": "archive/platform-macos-b992a4b",
        "import_tag": "import/platform-macos-b992a4b",
        "bundle": "/Volumes/NVME/GitHub/Aeostara-closeout-evidence/bundles/aeostara-platform-macos-b992a4b.bundle",
        "bundle_sha256": "408c553b8a2e1536898b46d3438c69111236dee6502d02ca3a9c6f1b4afe6c5f",
        "required_workflows": {
            ".github/workflows/macos-build.yml",
            ".github/workflows/downstream-conformance.yml",
            ".github/workflows/workflow-integrity.yml",
            ".github/workflows/attribution-integrity.yml",
        },
    },
    "platform/ios": {
        "destination_repo": "flynn33/Aeostara-Mac-iOS",
        "destination_branch": "platform/ios",
        "source_head": "0c931a7cbac349c6be93a6aeb4a253dd2268178f",
        "source_tree": "2d45c54b7363f9e1205b597f814074c445e09025",
        "commit_count": 18,
        "archive_tag": "archive/platform-ios-0c931a7",
        "import_tag": "import/platform-ios-0c931a7",
        "bundle": "/Volumes/NVME/GitHub/Aeostara-closeout-evidence/bundles/aeostara-platform-ios-0c931a7.bundle",
        "bundle_sha256": "ae2ff2d422359919b11a7374ce7b6a90bd779e73c7692e7329f77808b604a680",
        "required_workflows": {
            ".github/workflows/ios-build.yml",
            ".github/workflows/downstream-conformance.yml",
            ".github/workflows/workflow-integrity.yml",
            ".github/workflows/attribution-integrity.yml",
        },
    },
}
APPLE_COORDINATION_WORKFLOWS = {
    ".github/workflows/repository-integrity.yml",
    ".github/workflows/workflow-integrity.yml",
    ".github/workflows/attribution-integrity.yml",
}


@dataclass(frozen=True)
class BranchCapture:
    head: str
    tree: str
    count: int
    commits: set[str]


class RepositorySeparationChecker:
    def __init__(self, root: Path, online: bool, pre_cutover: bool) -> None:
        self.root = root
        self.online = online
        self.pre_cutover = pre_cutover

    def validate(self) -> list[str]:
        failures: list[str] = []
        final_base_commit = self._release_commit()
        source = {}
        for branch, spec in SOURCE_BRANCHES.items():
            capture = self._capture_commit(spec["source_head"])
            source[branch] = capture
            if capture.tree != spec["source_tree"]:
                failures.append(f"{branch}: captured tree mismatch {capture.tree} != {spec['source_tree']}")
            if capture.count != spec["commit_count"]:
                failures.append(f"{branch}: captured commit count mismatch {capture.count} != {spec['commit_count']}")
            failures.extend(self._validate_local_archive_and_bundle(branch, capture))
        if self.online:
            failures.extend(self._validate_online(source, final_base_commit))
        return failures

    def _validate_online(self, source: dict[str, BranchCapture], final_base_commit: str) -> list[str]:
        failures: list[str] = []
        for repo in sorted({str(item["destination_repo"]) for item in SOURCE_BRANCHES.values()}):
            repo_data = self._gh_json(["repo", "view", repo, "--json", "nameWithOwner,visibility,defaultBranchRef"])
            if repo_data is None:
                failures.append(f"destination repository missing or inaccessible: {repo}")
                continue
            if repo_data.get("visibility") != "PRIVATE":
                failures.append(f"{repo}: visibility must preserve PRIVATE source visibility")
            default_branch = (repo_data.get("defaultBranchRef") or {}).get("name")
            if repo == "flynn33/Aeostara-Windows" and default_branch != "main":
                failures.append(f"{repo}: default branch must be main")
            if repo == "flynn33/Aeostara-Mac-iOS" and default_branch != "main":
                failures.append(f"{repo}: default branch must be coordination main")
        for branch, spec in SOURCE_BRANCHES.items():
            src = source[branch]
            repo = str(spec["destination_repo"])
            dest_branch = str(spec["destination_branch"])
            archive_tag = str(spec["archive_tag"])
            import_tag = str(spec["import_tag"])
            dest_branch_capture = self._remote_branch_capture(repo, dest_branch)
            if dest_branch_capture is None:
                failures.append(f"{repo}:{dest_branch}: missing destination branch")
                continue
            import_capture = self._remote_tag_capture(repo, import_tag)
            if import_capture is None:
                failures.append(f"{repo}: missing import tag {import_tag}")
            elif import_capture != src:
                failures.append(f"{repo}:{import_tag}: import tag does not match source branch capture")
            elif not self._is_ancestor(src.head, dest_branch_capture.head):
                failures.append(f"{repo}:{dest_branch}: imported commit is not an ancestor of branch head")
            if not self._remote_ref_exists(SOURCE_REPOSITORY, f"refs/tags/{archive_tag}"):
                failures.append(f"source missing archive tag {archive_tag}")
            if self._remote_tag_commit(SOURCE_REPOSITORY, archive_tag) != src.head:
                failures.append(f"source archive tag {archive_tag} does not resolve to captured head")
            failures.extend(self._validate_branch_tree(repo, dest_branch_capture.head, spec["required_workflows"]))
            failures.extend(self._validate_base_pin(repo, dest_branch_capture.head, final_base_commit))
            failures.extend(self._validate_branch_protection(repo, dest_branch))
        failures.extend(self._validate_apple_coordination_main())
        for branch in SOURCE_BRANCHES:
            branch_exists = self._remote_ref_exists(SOURCE_REPOSITORY, f"refs/heads/{branch}")
            if self.pre_cutover and not branch_exists:
                failures.append(f"source platform branch missing before approved cutover: {branch}")
            if not self.pre_cutover and branch_exists:
                failures.append(f"source platform branch remains after cutover: {branch}")
        return failures

    def _validate_local_archive_and_bundle(self, branch: str, source: BranchCapture) -> list[str]:
        spec = SOURCE_BRANCHES[branch]
        failures: list[str] = []
        archive_tag = str(spec["archive_tag"])
        if self._git_optional(["rev-parse", "--verify", f"refs/tags/{archive_tag}^{{commit}}"]) != source.head:
            failures.append(f"{branch}: local archive tag {archive_tag} does not resolve to captured head")
        bundle_path = Path(str(spec["bundle"]))
        if not bundle_path.is_file():
            failures.append(f"{branch}: missing bundle {bundle_path}")
        else:
            actual_hash = self._sha256(bundle_path)
            expected_hash = str(spec["bundle_sha256"])
            if actual_hash != expected_hash:
                failures.append(f"{branch}: bundle hash mismatch {actual_hash} != {expected_hash}")
            verify = subprocess.run(["git", "bundle", "verify", str(bundle_path)], cwd=self.root, text=True, capture_output=True)
            if verify.returncode != 0:
                failures.append(f"{branch}: bundle verification failed")
            heads = self._git_optional(["bundle", "list-heads", str(bundle_path)])
            if source.head not in heads:
                failures.append(f"{branch}: bundle does not list captured head")
        return failures

    def _validate_branch_tree(self, repo: str, head: str, required_workflows: object) -> list[str]:
        failures: list[str] = []
        paths = set(self._git(["ls-tree", "-r", "--name-only", head]).splitlines())
        for required in sorted(required_workflows):
            if required not in paths:
                failures.append(f"{repo}:{head[:7]} missing workflow {required}")
        for rel in [FINAL_BASE_PIN_FILE, "MIGRATION_PROVENANCE.md"]:
            if rel not in paths:
                failures.append(f"{repo}:{head[:7]} missing {rel}")
        return failures

    def _validate_base_pin(self, repo: str, head: str, final_base_commit: str) -> list[str]:
        failures: list[str] = []
        text = self._git_optional(["show", f"{head}:{FINAL_BASE_PIN_FILE}"])
        if not text:
            return failures
        for required in [SOURCE_REPOSITORY, final_base_commit, REQUIRED_RELEASE_TAG, ASH_BASELINE_COMMIT]:
            if required not in text:
                failures.append(f"{repo}:{head[:7]} base pin missing {required}")
        return failures

    def _validate_branch_protection(self, repo: str, branch: str) -> list[str]:
        failures: list[str] = []
        protection = self._gh_api_json(f"repos/{repo}/branches/{quote(branch, safe='')}/protection")
        if protection is None:
            failures.append(f"{repo}:{branch}: missing branch protection")
            return failures
        if not protection.get("required_pull_request_reviews"):
            failures.append(f"{repo}:{branch}: pull-request review protection missing")
        if not protection.get("required_status_checks"):
            failures.append(f"{repo}:{branch}: required status checks missing")
        if protection.get("allow_force_pushes", {}).get("enabled"):
            failures.append(f"{repo}:{branch}: force pushes are allowed")
        if protection.get("allow_deletions", {}).get("enabled"):
            failures.append(f"{repo}:{branch}: deletion is allowed")
        return failures

    def _validate_apple_coordination_main(self) -> list[str]:
        failures: list[str] = []
        capture = self._remote_branch_capture("flynn33/Aeostara-Mac-iOS", "main")
        if capture is None:
            return ["flynn33/Aeostara-Mac-iOS:main: missing coordination branch"]
        paths = set(self._git(["ls-tree", "-r", "--name-only", capture.head]).splitlines())
        for required in APPLE_COORDINATION_WORKFLOWS:
            if required not in paths:
                failures.append(f"flynn33/Aeostara-Mac-iOS:main missing workflow {required}")
        implementation_markers = [
            path for path in paths
            if path.endswith((".swift", ".xcodeproj/project.pbxproj", ".cpp", ".h", ".hpp", ".m", ".mm"))
        ]
        if implementation_markers:
            failures.append("flynn33/Aeostara-Mac-iOS:main contains implementation source")
        failures.extend(self._validate_branch_protection("flynn33/Aeostara-Mac-iOS", "main"))
        return failures

    def _release_commit(self) -> str:
        release = self._git_optional(["rev-parse", "--verify", f"refs/tags/{REQUIRED_RELEASE_TAG}^{{commit}}"])
        if release:
            return release
        return self._git(["rev-parse", "HEAD"])

    def _capture_commit(self, commit: str) -> BranchCapture:
        head = self._git(["rev-parse", commit])
        tree = self._git(["rev-parse", f"{head}^{{tree}}"])
        count = int(self._git(["rev-list", "--count", head]))
        commits = set(self._git(["rev-list", head]).splitlines())
        return BranchCapture(head=head, tree=tree, count=count, commits=commits)

    def _remote_branch_capture(self, repo: str, branch: str) -> BranchCapture | None:
        url = f"https://github.com/{repo}.git"
        head = self._git_optional(["ls-remote", url, f"refs/heads/{branch}"])
        if not head:
            return None
        sha = head.split()[0]
        return self._capture_remote_commit_set(url, sha)

    def _remote_tag_capture(self, repo: str, tag: str) -> BranchCapture | None:
        commit = self._remote_tag_commit(repo, tag)
        if not commit:
            return None
        return self._capture_remote_commit_set(f"https://github.com/{repo}.git", commit)

    def _capture_remote_commit_set(self, url: str, sha: str) -> BranchCapture:
        self._git(["fetch", "--quiet", url, sha])
        tree = self._git(["rev-parse", f"{sha}^{{tree}}"])
        count = int(self._git(["rev-list", "--count", sha]))
        commits = set(self._git(["rev-list", sha]).splitlines())
        return BranchCapture(head=sha, tree=tree, count=count, commits=commits)

    def _remote_ref_exists(self, repo: str, ref: str) -> bool:
        url = f"https://github.com/{repo}.git"
        return bool(self._git_optional(["ls-remote", url, ref]))

    def _remote_tag_commit(self, repo: str, tag: str) -> str:
        url = f"https://github.com/{repo}.git"
        raw = self._git_optional(["ls-remote", "--tags", url, tag, f"{tag}^{{}}"])
        if not raw:
            return ""
        lines = raw.splitlines()
        peeled = [line for line in lines if line.endswith(f"refs/tags/{tag}^{{}}")]
        selected = peeled[0] if peeled else lines[0]
        return selected.split()[0]

    def _is_ancestor(self, ancestor: str, descendant: str) -> bool:
        try:
            subprocess.check_call(
                ["git", "merge-base", "--is-ancestor", ancestor, descendant],
                cwd=self.root,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def _gh_json(self, args: list[str]) -> dict[str, object] | None:
        try:
            raw = subprocess.check_output(["gh", *args], cwd=self.root, text=True, stderr=subprocess.DEVNULL)
            return json.loads(raw)
        except Exception:
            return None

    def _gh_api_json(self, endpoint: str) -> dict[str, object] | None:
        try:
            raw = subprocess.check_output(["gh", "api", endpoint], cwd=self.root, text=True, stderr=subprocess.DEVNULL)
            return json.loads(raw)
        except Exception:
            return None

    def _git(self, args: list[str]) -> str:
        return subprocess.check_output(["git", *args], cwd=self.root, text=True).strip()

    def _git_optional(self, args: list[str]) -> str:
        try:
            return self._git(args)
        except subprocess.CalledProcessError:
            return ""

    def _sha256(self, path: Path) -> str:
        import hashlib

        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Aeostara repository separation")
    parser.add_argument("repo_root", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--read-only", action="store_true")
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--pre-cutover", action="store_true", help="Require source platform branches to still exist")
    args = parser.parse_args()
    root = repo_root_from_arg([sys.argv[0], args.repo_root], __file__)
    failures = RepositorySeparationChecker(root, args.online, args.pre_cutover).validate()
    return print_result("repository separation", failures, "PASS: repository separation audit passed.")


if __name__ == "__main__":
    raise SystemExit(main())
