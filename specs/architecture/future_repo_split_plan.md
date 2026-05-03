# Future Repository Split Plan

Status: planning only.

## Target Structure

| Repository | Purpose |
|---|---|
| `aeostara-conformance-spec` | Downstream ASH conformance contracts, algorithms, acceptance, CI gates |
| `aeostara-windows` | Windows native realization |
| `aeostara-macos` | macOS native realization |
| `aeostara-ios` | iOS native realization |

## Migration Principle

The split must maintain the authority hierarchy:

- ASH upstream semantic source of truth
- Aeostara conformance specs downstream
- Platform repos as native realization layers

## Pre-Split Requirements

1. Conformance artifacts and traceability matrix finalized.
2. CI checks detect semantic-authority regressions.
3. Platform repos consume conformance artifacts without local semantic forks.
