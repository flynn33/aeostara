# Aeostara

**Deterministic JSON Configuration Drift Detection & Healing Platform v0.1**

*Authority / Specification Repository*

---

## Repository Role

This repository is the **platform-agnostic, language-agnostic authority** for Aeostara behavioral specifications. It defines *what* Aeostara must do, not *how* any specific platform implements it.

Platform implementations are planned to move to separate repositories (see [Future Repo Split Plan](specs/architecture/future_repo_split_plan.md)). Until that separation occurs, platform branches (`platform/windows`, `platform/macos`, `platform/ios`) exist within this repository as interim implementation homes.

## What This Repository Contains

| Category | Location | Description |
|----------|----------|-------------|
| Contracts | `specs/contracts/` | 11 JSON Schema behavioral contracts |
| Algorithms | `specs/algorithms/` | 9 pseudo-code algorithm definitions |
| Interfaces | `specs/interfaces/` | 5 pseudo-code interface definitions |
| Architecture | `specs/architecture/` | Architecture docs, branching strategy, compliance rules, planning |
| Acceptance | `specs/acceptance/` | Shared acceptance targets and compliance checklists |
| Fixtures | `fixtures/` | Shared deterministic test fixtures |
| CI Automation | `ci/` | Schema validation, acceptance running, compliance checking |

## What This Repository Does NOT Contain

- Compilable source code in any language
- Platform-specific build systems or toolchains
- Platform-specific runtime dependencies
- Completed Agnostic Core design (deferred to next phase)
- Direct Forsetti integration code

## Product Stack

Aeostara is part of a layered product architecture:

- **Aeostara** -- Deterministic JSON configuration drift detection, policy evaluation, repair planning, verification, rollback, and audit. The customer-facing product behavior.
- **ASH Pattern System** -- The healing kernel that provides encoded state models, drift semantics, and correction concepts. Aeostara v0.1 is ASH-inspired; full ASH formalization is deferred.
- **Forsetti Framework** -- The host/runtime framework providing shell, lifecycle, modules, plugins, and entitlements. Aeostara integrates with Forsetti at the platform implementation level, not at the root specification level.

See [Product Boundaries](specs/architecture/product_boundaries.md) for detailed boundary definitions.

## Non-Negotiable Product Constraints

These constraints apply to **all** platform implementations:

1. **Native-only shipped product** -- compiled native binaries, no interpreted runtimes
2. **JSON-only configuration** -- v0.1 uses JSON exclusively for configuration data
3. **No Python in shipped product** -- Python is permitted only for repo automation
4. **No YAML in shipped product** -- no YAML parser in any shipped product path
5. **Deterministic behavior** -- same input must produce same output across all platforms
6. **Policy / Backup / Verification / Rollback / Audit** -- mandatory behavioral constraints for every platform implementation

See [Compliance Rules](specs/architecture/compliance_rules.md) and [Agentic Coding Policy](agentic-coding-policy.json) for enforcement details.

## Current Platform Status

Platform implementations currently exist as branches within this repository:

| Branch | Status | Build Verified |
|--------|--------|----------------|
| `platform/windows` | Reference implementation | Locally proven |
| `platform/macos` | Source present | Build unverified |
| `platform/ios` | Source present | Build unverified |

Platform verification and release readiness will become the responsibility of future platform repositories. See [Platform Status Matrix](PLATFORM_STATUS_MATRIX.md) for details.

## Deferred Work

The following work is explicitly **not in scope** for the current phase:

- **Agnostic Core design** -- the next major phase after repository realignment
- **ASH/Ennea deepening** -- separate track from v0.1 product delivery (see [Roadmap Separation](specs/architecture/roadmap_separation.md))
- **Platform build verification** -- deferred to future platform repos
- **Direct Forsetti integration** -- deferred to platform implementation level
- **Planned Agnostic Core files** -- registered but not yet created (see [Planned File Index](specs/algorithms/PLANNED_AGNOSTIC_CORE_FILE_INDEX.md))

## License

Copyright (c) 2026 James Daley. All Rights Reserved. Proprietary. See [LICENSE.md](LICENSE.md).
