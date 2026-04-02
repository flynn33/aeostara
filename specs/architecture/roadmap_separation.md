# Roadmap Separation

This document separates the two development tracks that were previously blended in root-level planning. These tracks are independent: v0.1 product delivery does not require ASH Pattern System deepening, and ASH Pattern System deepening does not block v0.1 product verification.

---

## Track A — Aeostara v0.1 Product Delivery

### Scope
Deterministic JSON configuration drift detection and healing, delivered as a native compiled binary per platform.

### Core Behaviors
- Policy gating
- Backup before mutation
- Drift detection and analysis
- Repair planning and execution
- Post-repair verification
- Rollback on verification failure
- Audit trail

### Deliverable
A native compiled binary on each target platform implementing all 5 acceptance scenarios defined in `specs/acceptance/acceptance_targets.md`.

### Current State
- **Windows**: Reference implementation locally proven (build + test)
- **macOS**: Source present, build unverified
- **iOS**: Source present, build unverified

### Next Milestones
1. Repository realignment (this phase — in progress)
2. Platform verification in future platform repos (Windows CI, macOS/iOS build proof)
3. Release readiness per platform

---

## Track B — ASH Pattern System Deepening

### Scope
Formalization and deepening of the ASH Pattern System within Aeostara Core.

### Planned Work (Deferred)
- Encoded state model formalization
- Drift distance metric specification
- Correction semantics specification
- Confidence model specification
- Pattern reasoning specification
- Self-modeling concepts

### Status
**Deferred.** This work does not begin until:
1. Repository realignment is complete (this phase)
2. Agnostic Core design phase is complete (next phase)

### Dependency
ASH Pattern System deepening requires a completed Agnostic Core design to provide the abstraction layer where these concepts are formally defined.

---

## Track Independence

These tracks are **separate and independent**:

- v0.1 product delivery proceeds without waiting for ASH Pattern System deepening
- ASH Pattern System deepening proceeds without waiting for v0.1 platform release
- Neither track blocks the other
- Both tracks share the root specification authority in this repository

The Agnostic Core design phase (next after repository realignment) may draw from both tracks but is itself a separate planning effort.
