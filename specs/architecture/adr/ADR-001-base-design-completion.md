# ADR-001: Complete the Aeostara Platform-Agnostic Base Design

## Status

Authorized

## Date

2026-06-20

## Context

The Aeostara `main` branch contains the intended ASH authority model, contract inventory, lifecycle phases, JSON semantics, algorithms, interfaces, fixtures, and handoff structure. Several active interfaces and algorithms were abbreviated, and earlier validation proved artifact structure more strongly than executable semantic behavior.

## Decision

Complete the existing design without changing base semantics.

Authorized work includes elaborating existing interfaces and algorithms, strengthening semantic validation and executable conformance, correcting examples and fixtures, completing acceptance, traceability, handoff, documentation, wiki, and release evidence, and adding validation-only CI modules and tests.

The following remain immutable: ASH upstream semantics and baseline authority, existing contract fields and enum values, exactly nine ASH coordinates b0-b8, the fixed healing lifecycle, JSON Pointer and missing/null semantics, canonical JSON and SHA-256 identity, existing RecoveryCategory values, and the platform-agnostic scope of `main`.

## Consequences

Downstream teams receive deterministic implementable contracts. Conformance is established through executed expected-output evidence. Platform implementations remain independent and are migrated to authorized downstream repositories.

## Acceptance

This decision is complete only when the final release audit returns `CONFORMANT` with no caveats and contract hashes are unchanged.
