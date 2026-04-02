# Repository Role and Scope

## What This Repository Is

The **interim authority/specification repository** for Aeostara. It is the single source of truth for behavioral definitions that all platform implementations must satisfy.

This repository is:
- **Platform-agnostic** — it does not prescribe any platform-specific toolchain, language, or build system
- **Language-agnostic** — behavioral specifications are written in pseudo code, JSON Schema, and natural language
- **Behavior-authoritative** — contracts, algorithms, and interfaces defined here are binding on all platform implementations

## What This Repository Contains

| Category | Location | Description |
|----------|----------|-------------|
| Contracts | `specs/contracts/` | 11 JSON Schema behavioral contracts defining data types |
| Algorithms | `specs/algorithms/` | 9 pseudo-code algorithm definitions for healing flow, drift analysis, repair, etc. |
| Interfaces | `specs/interfaces/` | 5 pseudo-code interface definitions (IHealingEngine, IConfigAdapter, etc.) |
| Architecture | `specs/architecture/` | Architecture documentation, compliance rules, branching strategy, planning |
| Acceptance | `specs/acceptance/` | 5 shared acceptance scenarios and compliance checklists |
| Fixtures | `fixtures/` | 6 shared deterministic test fixture files |
| CI Automation | `ci/` | Schema validation, acceptance running, compliance checking (Python, exempt from product rules) |
| Governance | `agentic-coding-policy.json` | Platform-agnostic core specification policy |

## What This Repository Is NOT

- **Not a Windows implementation repo** — Windows implementation lives on `platform/windows` (planned: `aeostara-windows`)
- **Not a macOS implementation repo** — macOS implementation lives on `platform/macos` (planned: `aeostara-macos`)
- **Not an iOS implementation repo** — iOS implementation lives on `platform/ios` (planned: `aeostara-ios`)
- **Not the completed Agnostic Core design** — that is the next phase of work, deferred
- **Not the site of direct Forsetti integration work** — Forsetti integration happens at the platform implementation level

## Current State

Platform implementation branches exist within this repository as interim homes:
- `platform/windows` — reference implementation, locally proven
- `platform/macos` — source present, build unverified
- `platform/ios` — source present, build unverified

These branches will become separate repositories when the repo split is executed. See [Future Repo Split Plan](future_repo_split_plan.md).

## Future State

This repository will evolve into `aeostara-core-spec`, containing only platform-agnostic authority materials. Platform branches will become independent repositories with their own CI, build infrastructure, and release processes.

## Deferred Work

The following work is explicitly deferred from the current phase:

| Item | Dependency | Target Phase |
|------|-----------|-------------|
| Agnostic Core design | Repository realignment complete | Next phase |
| ASH/Ennea deepening | Agnostic Core design complete | Separate track (see [Roadmap Separation](roadmap_separation.md)) |
| Platform build verification | Platform repos established | Platform repo responsibility |
| Direct Forsetti integration | Platform repos established | Platform repo responsibility |
| Planned Agnostic Core files | Agnostic Core design phase | See [Planned File Index](../algorithms/PLANNED_AGNOSTIC_CORE_FILE_INDEX.md) |
