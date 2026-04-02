# Future Repository Split Plan

## Status: Planning Only

This document describes the planned separation of the current repository into multiple repositories. **No migration has been attempted.** This is a planning document.

---

## Target Repository Structure

| Repository | Source | Purpose |
|------------|--------|---------|
| `aeostara-core-spec` | Current `main` branch | Platform-agnostic authority: specs, contracts, algorithms, interfaces, acceptance targets, compliance rules, fixtures |
| `aeostara-windows` | Current `platform/windows` branch | Windows native implementation, build infrastructure, CI, release packaging |
| `aeostara-macos` | Current `platform/macos` branch | macOS native implementation, build infrastructure, CI, release packaging |
| `aeostara-ios` | Current `platform/ios` branch | iOS native implementation, build infrastructure, CI, release packaging |

## What Moves Where

### Core Spec Repo (`aeostara-core-spec`) Retains

- `specs/contracts/` — JSON Schema behavioral contracts
- `specs/algorithms/` — Pseudo-code algorithm definitions
- `specs/interfaces/` — Pseudo-code interface definitions
- `specs/architecture/` — Architecture documentation and planning
- `specs/acceptance/` — Shared acceptance targets
- `fixtures/` — Shared deterministic test fixtures
- `ci/` — Schema validation and compliance checking automation
- `agentic-coding-policy.json` — Root governance policy
- Root documentation (README, CHANGELOG, LICENSE)

### Each Platform Repo Receives

- Full source tree from its platform branch
- Platform-specific build system configurations
- Platform-specific CI workflows
- Platform-specific test infrastructure
- Platform manifest and documentation
- Platform-specific compliance documentation (toolchain rules, build flags)

### Shared Fixtures

Shared test fixtures (`fixtures/`) must remain accessible to all platform repos. Options for the split:

1. **Submodule** — each platform repo includes `aeostara-core-spec` as a Git submodule
2. **Package** — fixtures published as a consumable package
3. **Manual sync** — fixtures copied and kept in sync manually

The consumption mechanism will be decided during the actual split execution.

## Migration Approach

When the split is executed:

1. Extract each platform branch into its own repository (preserving git history if possible)
2. Clean the core spec repo to contain only `main` branch content
3. Set up cross-repo spec consumption (submodule, package, or sync)
4. Establish independent CI pipelines per platform repo
5. Update all cross-references and documentation links

## Prerequisites for Split

The following must be true before executing the split:

- [ ] Repository realignment complete (this phase)
- [ ] Agnostic Core design complete (next phase)
- [ ] Core spec repo content stable and validated
- [ ] Platform repos can independently consume the core spec
- [ ] Migration plan reviewed and approved

## What This Phase Does

This phase (repository realignment) **prepares** for the split by:

- Documenting the target structure (this file)
- Defining what belongs in each repository
- Removing root-level platform prescriptions
- Making the root specs genuinely platform-agnostic

This phase does **not** execute the actual repository migration.
