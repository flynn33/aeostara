# Downstream ASH Conformance Checklist

## Authority and Architecture

- [x] `REMEDIATION_STATUS.md` exists and declares ASH upstream authority.
- [x] `specs/architecture/ash_authority_and_aeostara_conformance.md` exists.
- [x] Root and architecture docs describe Aeostara as downstream conformance layer.
- [x] Legacy semantic authority language removed or marked historical.

## Contracts

- [x] ASH-aligned contract set exists for observed state, intent, semantic state, diagnostics, classification, recoverability, recovery plan, fallback, containment, safe halt.
- [x] Legacy drift-first contracts are marked `x-status: legacy-non-authoritative`.
- [x] Helper contracts (backup/rollback/verification/audit/module manifest) align to downstream flow.

## Algorithms

- [x] Normalization and mapping algorithms present.
- [x] Diagnosis/classification/recoverability algorithms present.
- [x] Recovery planning is recoverability-driven.
- [x] Fallback/containment/safe-halt algorithms present.
- [x] Execution/verification algorithm present.
- [x] Legacy drift/repair algorithms are non-authoritative helpers.

## Acceptance and Traceability

- [x] `ash_conformance_targets.md` exists.
- [x] `traceability_matrix.md` exists.
- [x] `remediation_acceptance_targets.md` exists.
- [x] Acceptance scenarios cover semantic-vs-diff mismatch and escalation behavior.
- [x] `branch_alignment_targets.md` exists.

## CI Enforcement

- [x] Schema validator checks required ASH-aligned contracts.
- [x] Compliance checker validates conformance artifacts and legacy markings.
- [x] Acceptance runner validates acceptance/traceability artifact completeness.
- [x] Branch alignment checker validates active branch profile invariants.
