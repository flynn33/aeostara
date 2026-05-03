# ASH Authority and Aeostara Conformance

## Purpose

This document defines the non-negotiable authority hierarchy and conformance boundaries for Aeostara.

## Authority Hierarchy

1. ASH semantic specifications (upstream authority)
2. Aeostara downstream conformance artifacts
3. Aeostara product execution mechanics

When conflict exists, ASH semantics are authoritative and Aeostara must change.

## What Aeostara Owns

Aeostara owns downstream adaptation and execution mechanics:

- Runtime observation ingestion
- State normalization adapters
- Mapping from product/runtime state into ASH-aligned semantic inputs
- Policy gating
- Backup/rollback mechanics
- Execution of approved actuator steps
- Verification and audit orchestration

These mechanics must consume ASH-derived diagnostics and classification outputs; they must not redefine semantic truth.

## What Aeostara Does Not Own

Aeostara is not authoritative for:

- Base state validity semantics
- System-state class semantics
- Recoverability category semantics
- Fallback policy semantics
- Containment and safe-halt semantics
- Rule taxonomy or diagnostic envelope semantics

## Mandatory Downstream Contract Layer

Aeostara must maintain contracts that adapt product mechanics to ASH semantics:

- Observed system state
- Desired system intent
- ASH semantic state
- State-validity diagnostic
- System-state class
- Recovery category
- Recovery plan
- Fallback decision
- Containment decision
- Safe-halt decision

## Mandatory Downstream Algorithm Layer

Aeostara must maintain deterministic algorithms for:

- State normalization
- State-to-ASH mapping
- ASH diagnostic evaluation
- State classification
- Recovery-category selection
- Recovery-plan generation
- Fallback selection
- Containment decisioning
- Safe-halt decisioning
- Execution-and-verification orchestration

## Prohibited Patterns

- Generic drift map as semantic authority
- Diff-to-CRUD planning as top-level recovery model
- Rule-expression engine as substitute for ASH validity/admissibility
- Semantic claims that position ASH as a subsystem of Aeostara

## Acceptance Requirement

Conformance is complete only when acceptance artifacts demonstrate ASH authority, downstream execution boundaries, and absence of drift/diff semantic authority.
