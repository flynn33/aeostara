# Changelog

All notable changes to Aeostara will be documented in this file.

## [0.3.0] - 2026-04-02

### Changed — Repository Realignment

- **Repositioned root as authority/specification repo** — README rewritten to define this repository as the platform-agnostic, language-agnostic behavioral authority
- **Replaced root governance policy** — `agentic-coding-policy.json` replaced from Windows-specific implementation policy to platform-agnostic core-spec policy (schemaVersion 2.0)
- **Resolved contradictory status language** — archived Phase 5 closeout, rewrote Platform Status Matrix with honest build verification states
- **Separated roadmaps** — created `roadmap_separation.md` splitting v0.1 product track from ASH/Ennea deepening track
- **Aligned acceptance and compliance docs** — removed platform-specific toolchain prescriptions from root architecture docs
- **Added future repo split preparation** — created `repo_role_and_scope.md` and `future_repo_split_plan.md` documenting planned separation into `aeostara-core-spec`, `aeostara-windows`, `aeostara-macos`, `aeostara-ios`
- **Registered deferred planning files** — created `PLANNED_AGNOSTIC_CORE_FILE_INDEX.md` for future Agnostic Core design phase

### Note

This release does not add new specifications, algorithms, or interfaces. It normalizes the repository identity and governance in preparation for the Agnostic Core design phase.

## [0.2.0] - 2026-03-21

### Added

- **Specification-first branch model**: `main` holds platform-agnostic specs, `platform/*` branches hold native implementations
- **11 JSON Schema contract definitions** in `specs/contracts/`
- **9 pseudo code algorithm specs** in `specs/algorithms/` (healing flow, drift analysis, repair planning, etc.)
- **5 interface pseudo code specs** in `specs/interfaces/` (IHealingEngine, IConfigAdapter, IBackupProvider, IAuditSink, IFileSystem)
- **Architecture documents** in `specs/architecture/` (boundaries, branching strategy, compliance rules, native target architecture)
- **Acceptance targets and compliance checklist** in `specs/acceptance/`
- **Shared test fixtures** in `fixtures/`
- **CI scripts** (Python) for schema validation, acceptance testing, and compliance checking
- **Platform branches**: `platform/windows` (reference implementation, locally proven), `platform/macos` (source present, build-unverified), `platform/ios` (source present, build-unverified)

### Changed

- Renamed `master` branch to `main`
- `main` branch now contains only specifications (no compilable source code)
- All C++20 source code moved to `platform/windows` branch

## [0.1.0] - 2026-03-20

### Added

- **Core Contracts**: 11 structs (ObservedState, DesiredState, EncodedState, DriftEvent, RepairAction, RepairPlan, VerificationResult, RollbackPlan, AuditEvent, ModuleManifest, Invariant) with nlohmann/json serialization
- **JsonPath**: Dot-path get/set/exists/flatten/unflatten for nested JSON
- **InvariantParser**: Load invariant rules from JSON files
- **DriftAnalyzer**: Compare encoded states, emit ValueChanged/KeyAdded/KeyRemoved drift events
- **RepairPlanner**: Generate deterministic repair plans with FNV-1a hashed plan IDs
- **PolicyEvaluator**: Expression-based invariant evaluation (==, !=, >, <, >=, <=) gating repair execution
- **BackupManager**: Timestamped file backups via IFileSystem abstraction
- **Verifier**: Post-repair verification against desired state and invariants
- **RollbackManager**: Automatic rollback from backup on verification failure
- **JsonLinesAuditTrail**: Append-only .jsonl audit logging
- **JsonConfigAdapter**: JSON config file read/encode/repair adapter
- **HealingEngine**: Central orchestrator implementing the full healing flow
- **CLI**: `aeostara validate|diff|heal` commands with `--desired`, `--invariants`, `--audit` options
- **Module-ready interfaces**: IHealingEngine, IConfigAdapter, IBackupProvider, IAuditSink, IFileSystem
- **CppUnitTest suite**: 14 test files covering all core components and 5 acceptance scenarios
- **Architecture enforcement tests**: Verify no Forsetti includes, all classes final, correct namespace, copyright headers
- **PowerShell verification scripts**: verify-aeostara-guardrails.ps1, check-architecture.ps1

### Technical Details (Windows Platform Branch)

> The v0.1.0 details below describe the Windows platform branch implementation. Platform-specific toolchain choices are documented here for historical context; they are not root-level prescriptions.

- C++20, CMake 3.28+, MSVC 2022, vcpkg
- Single dependency: nlohmann/json
- /W4 /WX (warnings as errors)
- JSON-only configuration scope
- Namespace: `Aeostara` (standalone, no Forsetti dependency)
