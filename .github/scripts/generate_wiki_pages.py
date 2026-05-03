#!/usr/bin/env python3
"""
Aeostara Wiki Page Generator
Builds branch-scoped, visually structured wiki pages from repo content.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass
class PageRef:
    title: str
    page_name: str  # without .md

    @property
    def markdown_link(self) -> str:
        return f"[{self.title}]({self.page_name})"


def sanitize_branch_slug(branch_name: str) -> str:
    slug = branch_name.replace("/", "__slash__").replace(" ", "-")
    slug = re.sub(r"[^A-Za-z0-9_.-]", "", slug)
    return slug


def title_from_filename(filename: str) -> str:
    stem = Path(filename).stem
    stem = stem.replace(".pseudo", "")
    stem = stem.replace(".schema", "")
    return " ".join(word.capitalize() for word in stem.replace("_", "-").split("-"))


def now_utc_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def cleanup_branch_pages(wiki_dir: Path, prefix: str) -> None:
    for file in wiki_dir.glob(f"{prefix}-*.md"):
        file.unlink(missing_ok=True)


def visual_context_for_source(source_rel: str, title: str) -> Tuple[str, str, List[Tuple[str, str]]]:
    """Return a compact visual frame for a wiki page based on its repo section."""
    if source_rel.startswith("specs/contracts/"):
        return (
            "Contract pages define the machine-checkable object shape that crosses a lifecycle boundary.",
            "\n".join(
                [
                    "flowchart LR",
                    '  Producer["Lifecycle producer"] --> Contract["Contract schema"]',
                    '  Contract --> Example["Schema example"]',
                    '  Example --> Validator["Schema validator"]',
                    '  Contract --> Fixture["Conformance fixture output"]',
                    '  Fixture --> Gate["Base-design gate"]',
                ]
            ),
            [
                ("Which lifecycle boundary uses it?", "Read `description`, required fields, and linked references."),
                ("What diagnostics are mandatory?", "Inspect diagnostic reference fields and rule-reference links."),
                ("How is it validated?", "Compare this schema with `fixtures/schema_examples/` and conformance vectors."),
            ],
        )
    if source_rel.startswith("specs/algorithms/"):
        return (
            "Algorithm pages define deterministic platform-neutral behavior that downstream repos implement behind native adapters.",
            "\n".join(
                [
                    "flowchart LR",
                    '  Input["Input contract"] --> Preconditions["Preconditions"]',
                    '  Preconditions --> Decision["Deterministic decision"]',
                    '  Decision --> Output["Output contract"]',
                    '  Decision --> Diagnostic["Diagnostic envelope"]',
                    '  Diagnostic --> Audit["Audit chain"]',
                ]
            ),
            [
                ("What is deterministic?", "Read the pseudocode branch table and preconditions."),
                ("What blocks unsafe behavior?", "Look for blocked, ambiguous, policy, or precondition paths."),
                ("How is the decision reconstructable?", "Trace diagnostic and audit requirements."),
            ],
        )
    if source_rel.startswith("specs/architecture/"):
        return (
            "Architecture pages define ownership, authority, and dependency direction for the base design.",
            "\n".join(
                [
                    "flowchart TB",
                    '  ASH["ASH fixed authority"] --> Aeostara["Aeostara base design"]',
                    '  Aeostara --> Contracts["Contracts and algorithms"]',
                    '  Aeostara --> Handoff["Downstream handoff"]',
                    '  Handoff --> Platforms["Windows / Mac / iOS repos"]',
                ]
            ),
            [
                ("Who owns the semantic decision?", "Check the authority and boundary language."),
                ("What is platform-neutral?", "Find Aeostara-owned obligations."),
                ("What moves downstream?", "Find adapter, implementation, and deviation rules."),
            ],
        )
    if source_rel.startswith("specs/acceptance/"):
        return (
            "Acceptance pages define the evidence needed before Aeostara or a downstream repo may claim conformance.",
            "\n".join(
                [
                    "flowchart LR",
                    '  Artifact["Spec artifact"] --> Fixture["Expected-output fixture"]',
                    '  Fixture --> Validator["CI checker"]',
                    '  Validator --> Report["Audit report"]',
                    '  Report --> Judgment["Acceptance judgment"]',
                ]
            ),
            [
                ("What evidence is required?", "Read the gate table or scenario list."),
                ("What must fail when broken?", "Check negative fixture and diagnostic-chain requirements."),
                ("What judgment is allowed?", "Use only the documented final judgment values."),
            ],
        )
    if source_rel.startswith("specs/interfaces/"):
        return (
            "Interface pages describe adapter boundaries that platform repos implement without changing base semantics.",
            "\n".join(
                [
                    "flowchart LR",
                    '  Base["Aeostara contract"] --> Interface["Interface boundary"]',
                    '  Interface --> Native["Platform-native module"]',
                    '  Native --> Result["Contract result"]',
                    '  Result --> Diagnostics["Diagnostics and audit"]',
                ]
            ),
            [
                ("What must the adapter provide?", "Read purpose and boundary rules."),
                ("Which contracts flow through it?", "Look for named input/output schemas."),
                ("Where can platform behavior vary?", "Only behind the boundary, never in base semantics."),
            ],
        )
    return (
        "This page is part of the base-design evidence set and should be read in authority-stack order.",
        "\n".join(
            [
                "flowchart TB",
                '  ASH["ASH authority"] --> Aeostara["Aeostara base design"]',
                '  Aeostara --> Evidence["Contracts, algorithms, fixtures, CI"]',
                '  Evidence --> Handoff["Downstream implementation handoff"]',
            ]
        ),
        [
            ("What role does this page play?", "Read the summary and source content."),
            ("What does it constrain?", "Trace named contracts, algorithms, fixtures, or handoff docs."),
            ("How is it checked?", "Use the linked CI and conformance artifacts."),
        ],
    )


def render_source_markdown_page(
    title: str,
    source_rel: str,
    branch_name: str,
    commit_sha: str,
    overview_page: str,
    content: str,
    summary: Optional[str] = None,
) -> str:
    lines: List[str] = [
        f"# {title}",
        "",
        f"[Back to Branch Overview]({overview_page})",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Branch | `{branch_name}` |",
        f"| Source | `{source_rel}` |",
        f"| Commit | `{commit_sha[:12]}` |",
        f"| Synced (UTC) | {now_utc_iso()} |",
    ]
    if summary:
        lines += ["", f"> {summary}"]
    context_summary, diagram, checklist = visual_context_for_source(source_rel, title)
    lines += [
        "",
        "## Visual Context",
        "",
        f"> {context_summary}",
        "",
        "```mermaid",
        diagram,
        "```",
        "",
        "## Reading Checklist",
        "",
        "| Question | Where to look |",
        "|---|---|",
    ]
    lines.extend(f"| {question} | {target} |" for question, target in checklist)
    lines += ["", "---", "", "## Source Content", "", content.strip()]
    return "\n".join(lines)


def render_json_page(
    title: str,
    source_rel: str,
    branch_name: str,
    commit_sha: str,
    overview_page: str,
    json_text: str,
) -> str:
    context_summary, diagram, checklist = visual_context_for_source(source_rel, title)
    lines = [
        f"# {title}",
        "",
        f"[Back to Branch Overview]({overview_page})",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Branch | `{branch_name}` |",
        f"| Source | `{source_rel}` |",
        f"| Commit | `{commit_sha[:12]}` |",
        f"| Synced (UTC) | {now_utc_iso()} |",
        "",
        "## Visual Context",
        "",
        f"> {context_summary}",
        "",
        "```mermaid",
        diagram,
        "```",
        "",
        "## Reading Checklist",
        "",
        "| Question | Where to look |",
        "|---|---|",
    ]
    lines.extend(f"| {question} | {target} |" for question, target in checklist)
    lines += [
        "",
        "---",
        "",
        "## JSON Payload",
        "",
        "```json",
        json_text.rstrip(),
        "```",
    ]
    return "\n".join(lines)


def render_stub_page(
    title: str,
    source_rel: str,
    branch_name: str,
    commit_sha: str,
    overview_page: str,
    reason: str,
) -> str:
    context_summary, diagram, checklist = visual_context_for_source(source_rel, title)
    lines = [
        f"# {title}",
        "",
        f"[Back to Branch Overview]({overview_page})",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Branch | `{branch_name}` |",
        f"| Source | `{source_rel}` |",
        f"| Commit | `{commit_sha[:12]}` |",
        f"| Synced (UTC) | {now_utc_iso()} |",
        "",
        f"> {reason}",
        "",
        "## Visual Context",
        "",
        f"> {context_summary}",
        "",
        "```mermaid",
        diagram,
        "```",
        "",
        "## Reading Checklist",
        "",
        "| Question | Where to look |",
        "|---|---|",
    ]
    lines.extend(f"| {question} | {target} |" for question, target in checklist)
    return "\n".join(
        lines
    )


def write_wrapped_markdown(
    src_dir: Path,
    wiki_dir: Path,
    prefix: str,
    section: str,
    source_rel: str,
    title: str,
    branch_name: str,
    commit_sha: str,
    overview_page: str,
    summary: Optional[str] = None,
) -> PageRef:
    slug = Path(source_rel).stem.replace(".pseudo", "").replace(".schema", "").replace("_", "-")
    page_name = f"{prefix}-{section}-{slug}"
    target = wiki_dir / f"{page_name}.md"
    source_path = src_dir / source_rel
    if source_path.exists():
        content = render_source_markdown_page(
            title=title,
            source_rel=source_rel,
            branch_name=branch_name,
            commit_sha=commit_sha,
            overview_page=overview_page,
            content=load_text(source_path),
            summary=summary,
        )
    else:
        content = render_stub_page(
            title=title,
            source_rel=source_rel,
            branch_name=branch_name,
            commit_sha=commit_sha,
            overview_page=overview_page,
            reason=f"No source file found at `{source_rel}` on this branch.",
        )
    write_text(target, content)
    return PageRef(title=title, page_name=page_name)


def write_wrapped_json(
    src_dir: Path,
    wiki_dir: Path,
    prefix: str,
    section: str,
    source_rel: str,
    title: str,
    branch_name: str,
    commit_sha: str,
    overview_page: str,
) -> PageRef:
    slug = Path(source_rel).stem.replace(".schema", "").replace("_", "-")
    page_name = f"{prefix}-{section}-{slug}"
    target = wiki_dir / f"{page_name}.md"
    source_path = src_dir / source_rel
    if source_path.exists():
        content = render_json_page(
            title=title,
            source_rel=source_rel,
            branch_name=branch_name,
            commit_sha=commit_sha,
            overview_page=overview_page,
            json_text=load_text(source_path),
        )
    else:
        content = render_stub_page(
            title=title,
            source_rel=source_rel,
            branch_name=branch_name,
            commit_sha=commit_sha,
            overview_page=overview_page,
            reason=f"No source file found at `{source_rel}` on this branch.",
        )
    write_text(target, content)
    return PageRef(title=title, page_name=page_name)


def collect_paths(src_dir: Path, glob_pattern: str) -> List[Path]:
    return sorted([p for p in src_dir.glob(glob_pattern) if p.is_file()])


def maybe_generate_api_reference(src_dir: Path, temp_dir: Path, branch_name: str) -> Tuple[str, str]:
    api_path = temp_dir / "api_reference.md"

    cpp_include = src_dir / "include" / "AeostaraCore"
    cpp_include_alt = src_dir / "AeostaraCore" / "include" / "AeostaraCore"
    swift_package = src_dir / "Package.swift"

    if cpp_include.is_dir() or cpp_include_alt.is_dir():
        include_dir = cpp_include if cpp_include.is_dir() else cpp_include_alt
        parser = src_dir / ".github" / "scripts" / "parse-headers.py"
        subprocess.run(
            ["python3", str(parser), str(include_dir), str(api_path)],
            check=True,
        )
        return "C++ API Reference", load_text(api_path)

    if swift_package.is_file():
        parser = src_dir / ".github" / "scripts" / "parse-swift-modules.sh"
        subprocess.run(
            ["bash", str(parser), str(src_dir), str(api_path)],
            check=True,
            env={**os.environ, "BRANCH_NAME": branch_name},
        )
        return "Swift Module Reference", load_text(api_path)

    return "API Reference", "# API Reference\n\nNo public headers or Swift modules were found on this branch.\n"


def branch_profile_description(branch_name: str) -> str:
    if branch_name == "main":
        return "Platform-agnostic Aeostara base-design authority"
    if branch_name == "platform/windows":
        return "Windows downstream implementation repository"
    if branch_name == "platform/macos":
        return "Mac downstream implementation repository"
    if branch_name == "platform/ios":
        return "iOS downstream implementation repository"
    return "Feature/custom branch"


def list_top_level_dirs(src_dir: Path) -> List[str]:
    return sorted([p.name for p in src_dir.iterdir() if p.is_dir() and not p.name.startswith(".")])


def build_specs_index(src_dir: Path, wiki_dir: Path, prefix: str, branch_name: str, commit_sha: str, overview_page: str) -> PageRef:
    page_name = f"{prefix}-Specs-Index"
    target = wiki_dir / f"{page_name}.md"

    specs_root = src_dir / "specs"
    files: List[str] = []
    if specs_root.is_dir():
        files = sorted(str(p.relative_to(src_dir)) for p in specs_root.rglob("*") if p.is_file())

    lines: List[str] = [
        f"# Specs Index ({branch_name})",
        "",
        f"[Back to Branch Overview]({overview_page})",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Branch | `{branch_name}` |",
        f"| Commit | `{commit_sha[:12]}` |",
        f"| Synced (UTC) | {now_utc_iso()} |",
        f"| Total Spec Files | {len(files)} |",
        "",
        "---",
        "",
    ]

    if files:
        lines += ["## Files", ""]
        for item in files:
            lines.append(f"- `{item}`")
    else:
        lines += ["No `specs/` directory is present on this branch."]

    write_text(target, "\n".join(lines))
    return PageRef(title="Specs Index", page_name=page_name)


def write_api_page(
    src_dir: Path,
    wiki_dir: Path,
    prefix: str,
    branch_name: str,
    commit_sha: str,
    overview_page: str,
) -> PageRef:
    tmp_dir = wiki_dir / ".tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    title, api_body = maybe_generate_api_reference(src_dir, tmp_dir, branch_name)
    page_name = f"{prefix}-API-Reference"
    target = wiki_dir / f"{page_name}.md"

    wrapped = "\n".join(
        [
            f"# {title} ({branch_name})",
            "",
            f"[Back to Branch Overview]({overview_page})",
            "",
            "| Field | Value |",
            "|---|---|",
            f"| Branch | `{branch_name}` |",
            f"| Commit | `{commit_sha[:12]}` |",
            f"| Synced (UTC) | {now_utc_iso()} |",
            "",
            "---",
            "",
            api_body.strip(),
        ]
    )
    write_text(target, wrapped)
    return PageRef(title=title, page_name=page_name)


def write_branch_overview(
    wiki_dir: Path,
    prefix: str,
    branch_name: str,
    commit_sha: str,
    category_pages: Dict[str, List[PageRef]],
    specs_count: Dict[str, int],
    top_dirs: List[str],
) -> PageRef:
    page_name = f"{prefix}-Overview"
    target = wiki_dir / f"{page_name}.md"

    lines: List[str] = [
        f"# {branch_name} Branch Wiki",
        "",
        f"> {branch_profile_description(branch_name)}",
        "",
        "## Base-Design Navigation",
        "",
        "```mermaid",
        "flowchart TB",
        '  ASH["ASH Pattern System<br/>fixed upstream authority"] --> Base["Aeostara<br/>platform-agnostic base design"]',
        '  Base --> Contracts["Contract schemas"]',
        '  Base --> Algorithms["Deterministic algorithms"]',
        '  Base --> Fixtures["Expected-output fixtures"]',
        '  Base --> Handoff["Platform repo handoff"]',
        '  Contracts --> CI["Base conformance CI"]',
        '  Algorithms --> CI',
        '  Fixtures --> CI',
        '  Handoff --> Platforms["Windows / Mac / iOS repos"]',
        "```",
        "",
        "## Healing Lifecycle",
        "",
        "```mermaid",
        "flowchart LR",
        '  Observe["Observe JSON config"] --> Normalize["Normalize"]',
        '  Normalize --> Project["Project semantic dimensions"]',
        '  Project --> Bind["Bind to ASH state"]',
        '  Bind --> Diagnose["Diagnose"]',
        '  Diagnose --> Classify["Classify"]',
        '  Classify --> Recover["Recoverability"]',
        '  Recover --> Plan["Recovery plan"]',
        '  Plan --> Policy["Policy gate"]',
        '  Policy --> Backup["Backup"]',
        '  Backup --> Execute["Execute"]',
        '  Execute --> Verify["Verify"]',
        '  Verify --> Outcome["Rollback / fallback / containment / safe halt"]',
        '  Outcome --> Audit["Diagnostic + audit chain"]',
        "```",
        "",
        "## Conformance Gate Logic",
        "",
        "```mermaid",
        "flowchart LR",
        '  Schemas["Schemas + examples"] --> Runner["conformance_runner.py"]',
        '  Fixtures["Fixture vectors"] --> Runner',
        '  Trace["ASH traceability"] --> Runner',
        '  Json["JSON semantics"] --> Runner',
        '  Diag["Diagnostic chain"] --> Runner',
        '  Recovery["Recovery consistency"] --> Runner',
        '  Handoff["Downstream handoff"] --> Runner',
        '  Runner --> Judgment["CONFORMANT / CAVEATS / NON-CONFORMANT"]',
        "```",
        "",
        "## Snapshot",
        "",
        "| Property | Value |",
        "|---|---|",
        f"| Branch | `{branch_name}` |",
        f"| Commit | `{commit_sha[:12]}` |",
        f"| Synced (UTC) | {now_utc_iso()} |",
        f"| Profile | {branch_profile_description(branch_name)} |",
        "",
        "## Authority Map",
        "",
        "```mermaid",
        "flowchart LR",
        '  ASH["ASH Upstream Authority"] --> MAIN["Aeostara base design"]',
        f'  MAIN --> BRANCH["{branch_name}"]',
        "```",
        "",
        "## Coverage",
        "",
        "| Area | Count |",
        "|---|---:|",
        f"| Core Docs | {specs_count.get('core', 0)} |",
        f"| Architecture Docs | {specs_count.get('architecture', 0)} |",
        f"| Algorithms | {specs_count.get('algorithms', 0)} |",
        f"| Interfaces | {specs_count.get('interfaces', 0)} |",
        f"| Contracts | {specs_count.get('contracts', 0)} |",
        f"| Acceptance Docs | {specs_count.get('acceptance', 0)} |",
        "",
    ]

    for section in ["Core", "Platform", "Architecture", "Specifications", "API", "Status"]:
        refs = category_pages.get(section, [])
        if not refs:
            continue
        lines += [f"## {section}", ""]
        for ref in refs:
            lines.append(f"- {ref.markdown_link}")
        lines.append("")

    lines += ["## Repository Top-Level Folders", ""]
    for d in top_dirs:
        lines.append(f"- `{d}`")

    write_text(target, "\n".join(lines))
    return PageRef(title=f"{branch_name} Overview", page_name=page_name)


def parse_branch_index(index_path: Path) -> Dict[str, Tuple[str, str, str]]:
    rows: Dict[str, Tuple[str, str, str]] = {}
    if not index_path.exists():
        return rows
    for line in index_path.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        slug = parts[0]
        branch = parts[1]
        synced = parts[2] if len(parts) > 2 else ""
        commit = parts[3] if len(parts) > 3 else ""
        rows[slug] = (branch, synced, commit)
    return rows


def write_branch_index(index_path: Path, rows: Dict[str, Tuple[str, str, str]]) -> None:
    ordered = sorted(rows.items(), key=lambda item: item[1][0])
    lines = [f"{slug}\t{branch}\t{synced}\t{commit}" for slug, (branch, synced, commit) in ordered]
    write_text(index_path, "\n".join(lines) if lines else "")


def write_home_page(wiki_dir: Path, rows: Dict[str, Tuple[str, str, str]]) -> None:
    target = wiki_dir / "Home.md"
    lines: List[str] = [
        "# Aeostara Knowledge Base",
        "",
        "> Visual operating map for the Aeostara platform-agnostic base design.",
        "",
        "## System Map",
        "",
        "```mermaid",
        "flowchart TB",
        '  ASH["ASH Pattern System"] --> Base["Aeostara base design"]',
        '  Base --> Json["JSON semantics"]',
        '  Base --> AshBind["ASH bindings"]',
        '  Base --> Lifecycle["Healing lifecycle"]',
        '  Base --> Contracts["Contracts"]',
        '  Base --> CI["Conformance CI"]',
        '  Base --> Handoff["Downstream handoff"]',
        '  Handoff --> Win["Windows repo"]',
        '  Handoff --> Mac["Mac repo"]',
        '  Handoff --> Ios["iOS repo"]',
        "```",
        "",
        "## Core Logic",
        "",
        "```mermaid",
        "flowchart LR",
        '  Observe["Observe"] --> Normalize["Normalize"] --> Project["Project"] --> Diagnose["Diagnose"]',
        '  Diagnose --> Classify["Classify"] --> Plan["Plan recovery"] --> Gate["Policy gate"]',
        '  Gate --> Backup["Backup"] --> Execute["Execute"] --> Verify["Verify"]',
        '  Verify --> Safety["Rollback / fallback / containment / safe halt"] --> Audit["Audit chain"]',
        "```",
        "",
        "## Quick Start",
        "",
        "1. Open [Branch main Overview](Branch-main-Overview) for the full visual map.",
        "2. Use [Repository Overview](Repository-Overview) for the authority model and artifact taxonomy.",
        "3. Use [Runtime Logic and Workflows](Runtime-Logic-and-Workflows) for the observe-to-safe-halt operating logic.",
        "4. Use [ASH Conformance](ASH-Conformance) to trace ASH bindings, invariants, and fixture evidence.",
        "5. Use [Acceptance and CI](Acceptance-and-CI) to understand validation gates and command outputs.",
        "6. Use [Artifact Index](Artifact-Index) to jump directly to contracts, algorithms, interfaces, and acceptance pages.",
        "",
        "## Documentation Lanes",
        "",
        "| Lane | Purpose | Primary pages |",
        "|---|---|---|",
        "| Authority | Shows dependency direction and ownership boundaries | [Repository Overview](Repository-Overview), [Branch main Overview](Branch-main-Overview) |",
        "| ASH binding | Maps ASH source authority into Aeostara obligations | [ASH Conformance](ASH-Conformance), [Branch main Specs Index](Branch-main-Specs-Index) |",
        "| Runtime logic | Explains observe-to-safe-halt lifecycle | [Runtime Logic and Workflows](Runtime-Logic-and-Workflows), [Diagnostic Recovery Safety Logic](Diagnostic-Recovery-Safety-Logic) |",
        "| JSON and projection | Shows JSON Pointer, canonicalization, missing/null, and ASH coordinate projection | [JSON Semantics and Projection](JSON-Semantics-and-Projection) |",
        "| Contracts | Groups lifecycle schemas by responsibility | [Contract and Schema Atlas](Contract-and-Schema-Atlas), contract pages |",
        "| Evidence | Shows fixture, schema, and CI proof points | [Acceptance and CI](Acceptance-and-CI), conformance pages |",
        "| Handoff | Explains downstream Windows/Mac/iOS implementation obligations | [Downstream Handoff Guide](Downstream-Handoff-Guide), platform handoff templates |",
        "",
        "## Branch Dashboards",
        "",
        "| Branch | Overview | Last Sync (UTC) | Commit |",
        "|---|---|---|---|",
    ]

    for slug, (branch, synced, commit) in sorted(rows.items(), key=lambda item: item[1][0]):
        lines.append(
            f"| `{branch}` | [Open](Branch-{slug}-Overview) | {synced or '-'} | `{(commit or '')[:12] or '-'} `|"
        )

    lines += [
        "",
        "## Maintenance",
        "",
        "Wiki content is refreshed by repository workflows and the branch overview generator. Generated pages include visual context, checklist tables, source references, and direct artifact links.",
    ]

    write_text(target, "\n".join(lines))


def generate_for_branch(src_dir: Path, wiki_dir: Path, branch_name: str, commit_sha: str) -> None:
    slug = sanitize_branch_slug(branch_name)
    prefix = f"Branch-{slug}"
    overview_page = f"{prefix}-Overview"

    cleanup_branch_pages(wiki_dir, prefix)

    category_pages: Dict[str, List[PageRef]] = {
        "Core": [],
        "Platform": [],
        "Architecture": [],
        "Specifications": [],
        "API": [],
        "Status": [],
    }

    # Core docs
    core_docs = [
        ("README.md", "README"),
        ("CHANGELOG.md", "Changelog"),
        ("LICENSE.md", "License"),
        ("REMEDIATION_STATUS.md", "Remediation Status"),
    ]
    for rel, title in core_docs:
        ref = write_wrapped_markdown(
            src_dir=src_dir,
            wiki_dir=wiki_dir,
            prefix=prefix,
            section="Core",
            source_rel=rel,
            title=title,
            branch_name=branch_name,
            commit_sha=commit_sha,
            overview_page=overview_page,
        )
        category_pages["Core"].append(ref)

    # Status docs
    for rel, title in [
        ("PHASE_5_CLOSEOUT.md", "Phase 5 Closeout"),
        ("PLATFORM_STATUS_MATRIX.md", "Platform Status Matrix"),
    ]:
        ref = write_wrapped_markdown(
            src_dir=src_dir,
            wiki_dir=wiki_dir,
            prefix=prefix,
            section="Status",
            source_rel=rel,
            title=title,
            branch_name=branch_name,
            commit_sha=commit_sha,
            overview_page=overview_page,
        )
        category_pages["Status"].append(ref)

    # Platform docs
    for rel, title in [
        ("platform/windows/README.md", "Windows Platform README"),
        ("platform/macos/README.md", "macOS Platform README"),
        ("platform/ios/README.md", "iOS Platform README"),
        ("platform/ios/docs/platform_policy_apple.md", "Apple Platform Policy"),
    ]:
        if (src_dir / rel).exists():
            ref = write_wrapped_markdown(
                src_dir=src_dir,
                wiki_dir=wiki_dir,
                prefix=prefix,
                section="Platform",
                source_rel=rel,
                title=title,
                branch_name=branch_name,
                commit_sha=commit_sha,
                overview_page=overview_page,
            )
            category_pages["Platform"].append(ref)

    for rel, title in [
        ("platform/windows/PLATFORM_MANIFEST.json", "Windows Platform Manifest"),
        ("platform/macos/PLATFORM_MANIFEST.json", "macOS Platform Manifest"),
        ("platform/ios/PLATFORM_MANIFEST.json", "iOS Platform Manifest"),
    ]:
        if (src_dir / rel).exists():
            ref = write_wrapped_json(
                src_dir=src_dir,
                wiki_dir=wiki_dir,
                prefix=prefix,
                section="Platform",
                source_rel=rel,
                title=title,
                branch_name=branch_name,
                commit_sha=commit_sha,
                overview_page=overview_page,
            )
            category_pages["Platform"].append(ref)

    # Architecture
    for file in collect_paths(src_dir, "specs/architecture/*.md"):
        rel = str(file.relative_to(src_dir))
        title = title_from_filename(file.name)
        ref = write_wrapped_markdown(
            src_dir=src_dir,
            wiki_dir=wiki_dir,
            prefix=prefix,
            section="Arch",
            source_rel=rel,
            title=title,
            branch_name=branch_name,
            commit_sha=commit_sha,
            overview_page=overview_page,
        )
        category_pages["Architecture"].append(ref)

    # Algorithms
    for file in collect_paths(src_dir, "specs/algorithms/*.md"):
        rel = str(file.relative_to(src_dir))
        title = f"Algorithm: {title_from_filename(file.name)}"
        ref = write_wrapped_markdown(
            src_dir=src_dir,
            wiki_dir=wiki_dir,
            prefix=prefix,
            section="Algo",
            source_rel=rel,
            title=title,
            branch_name=branch_name,
            commit_sha=commit_sha,
            overview_page=overview_page,
        )
        category_pages["Specifications"].append(ref)

    # Interfaces
    for file in collect_paths(src_dir, "specs/interfaces/*.md"):
        rel = str(file.relative_to(src_dir))
        title = f"Interface: {title_from_filename(file.name)}"
        ref = write_wrapped_markdown(
            src_dir=src_dir,
            wiki_dir=wiki_dir,
            prefix=prefix,
            section="Interface",
            source_rel=rel,
            title=title,
            branch_name=branch_name,
            commit_sha=commit_sha,
            overview_page=overview_page,
        )
        category_pages["Specifications"].append(ref)

    # Contracts
    for file in collect_paths(src_dir, "specs/contracts/*.schema.json"):
        rel = str(file.relative_to(src_dir))
        title = f"Contract: {title_from_filename(file.name)}"
        ref = write_wrapped_json(
            src_dir=src_dir,
            wiki_dir=wiki_dir,
            prefix=prefix,
            section="Contract",
            source_rel=rel,
            title=title,
            branch_name=branch_name,
            commit_sha=commit_sha,
            overview_page=overview_page,
        )
        category_pages["Specifications"].append(ref)

    # Acceptance
    for file in collect_paths(src_dir, "specs/acceptance/*.md"):
        rel = str(file.relative_to(src_dir))
        title = f"Acceptance: {title_from_filename(file.name)}"
        ref = write_wrapped_markdown(
            src_dir=src_dir,
            wiki_dir=wiki_dir,
            prefix=prefix,
            section="Acceptance",
            source_rel=rel,
            title=title,
            branch_name=branch_name,
            commit_sha=commit_sha,
            overview_page=overview_page,
        )
        category_pages["Specifications"].append(ref)

    # API page
    api_ref = write_api_page(
        src_dir=src_dir,
        wiki_dir=wiki_dir,
        prefix=prefix,
        branch_name=branch_name,
        commit_sha=commit_sha,
        overview_page=overview_page,
    )
    category_pages["API"].append(api_ref)

    # Specs index page
    specs_index_ref = build_specs_index(
        src_dir=src_dir,
        wiki_dir=wiki_dir,
        prefix=prefix,
        branch_name=branch_name,
        commit_sha=commit_sha,
        overview_page=overview_page,
    )
    category_pages["Specifications"].append(specs_index_ref)

    specs_count = {
        "core": len(category_pages["Core"]),
        "architecture": len(category_pages["Architecture"]),
        "algorithms": len(collect_paths(src_dir, "specs/algorithms/*.md")),
        "interfaces": len(collect_paths(src_dir, "specs/interfaces/*.md")),
        "contracts": len(collect_paths(src_dir, "specs/contracts/*.schema.json")),
        "acceptance": len(collect_paths(src_dir, "specs/acceptance/*.md")),
    }

    overview_ref = write_branch_overview(
        wiki_dir=wiki_dir,
        prefix=prefix,
        branch_name=branch_name,
        commit_sha=commit_sha,
        category_pages=category_pages,
        specs_count=specs_count,
        top_dirs=list_top_level_dirs(src_dir),
    )

    # Update branch index + home
    index_path = wiki_dir / ".branch-index.tsv"
    rows = parse_branch_index(index_path)
    rows[slug] = (branch_name, now_utc_iso(), commit_sha)
    write_branch_index(index_path, rows)
    write_home_page(wiki_dir, rows)

    # Cleanup temp artifacts generated for API extraction.
    shutil.rmtree(wiki_dir / ".tmp", ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Aeostara wiki pages")
    parser.add_argument("--src-dir", required=True)
    parser.add_argument("--wiki-dir", required=True)
    parser.add_argument("--branch-name", required=True)
    parser.add_argument("--commit-sha", required=True)
    args = parser.parse_args()

    src_dir = Path(args.src_dir).resolve()
    wiki_dir = Path(args.wiki_dir).resolve()
    branch_name = args.branch_name.strip()
    commit_sha = args.commit_sha.strip()

    if not src_dir.is_dir():
        raise SystemExit(f"Source directory not found: {src_dir}")
    wiki_dir.mkdir(parents=True, exist_ok=True)

    generate_for_branch(src_dir, wiki_dir, branch_name, commit_sha)
    print(f"Generated wiki pages for {branch_name} at {commit_sha[:12]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
