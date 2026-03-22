# Aeostara

**Deterministic JSON Configuration Drift Detection and Healing Platform** - v0.1

Aeostara observes live configuration, compares it against a declared desired state, detects drift, evaluates invariant policy, and executes repairs with backup, verification, rollback, and audit trail.

Copyright (c) 2026 James Daley. All Rights Reserved.
Proprietary and Confidential.

## Branch Model

This repository uses a specification-first branch strategy:

| Branch | Purpose |
|--------|---------|
| `main` | Code-agnostic specifications: JSON contract schemas, pseudo code algorithms, interface definitions, architecture docs, test fixtures |
| `platform/windows` | Windows-native realization (C++20, MSVC, CMake, vcpkg) |
| `platform/macos` | macOS-native realization (Swift, SwiftPM, XCTest) |
| `platform/ios` | iOS-native realization (Swift, SwiftUI, SwiftPM, XCTest/XCUITest) |

`main` is code-agnostic and behavior-authoritative. Platform branches are **native realization branches** — they implement shared spec behavior using their platform's native toolchain and may integrate with their platform's Forsetti framework. Branch internals are not required to preserve `main`'s implementation-agnostic posture.

Spec changes on `main` merge down into platform branches. Platform code never merges back to `main`.

## Specifications

### Contracts (11 types)
JSON Schema definitions in `specs/contracts/`:
ObservedState, DesiredState, EncodedState, Invariant, DriftEvent, RepairAction, RepairPlan, VerificationResult, RollbackPlan, AuditEvent, ModuleManifest

### Algorithms (9)
Pseudo code in `specs/algorithms/`:
healing_flow, drift_analysis, repair_planning, policy_evaluation, json_path, verification, rollback, backup, audit

### Interfaces (5)
Pseudo code in `specs/interfaces/`:
IHealingEngine, IConfigAdapter, IBackupProvider, IAuditSink, IFileSystem

### Architecture
Design documents in `specs/architecture/`:
product_boundaries, branching_strategy, compliance_rules, native_target_architecture

## Product Stack

- **Aeostara** = product (customer-facing behavior, contracts, adapters)
- **ASH Pattern System** = healing kernel (encoded state, drift, correction semantics)
- **Forsetti Framework** = host/runtime framework (shell, lifecycle, UI)

## Compliance

- **Native only** — shipped product is a compiled native binary
- **JSON-only** — all configuration files are JSON; no YAML parser
- **No Python** — shipped product has no Python dependency
- **Forsetti-compliant** — spec behavior is code-agnostic; platform branches realize Aeostara natively per platform Forsetti rules
- **ASH-inspired** — healing semantics follow the Aeostara Self-Healing pattern

## Platform Targets

- **Windows** — C++20, MSVC 2022, CMake, vcpkg (`platform/windows`)
- **macOS** — Swift / SwiftPM native (`platform/macos`)
- **iOS** — Swift / SwiftUI native (`platform/ios`)

## License

Proprietary. All rights reserved. See [LICENSE.md](LICENSE.md).
