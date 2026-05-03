# Downstream ASH Conformance Checklist

## Authority and Architecture

- [x] `REMEDIATION_STATUS.md` exists and declares ASH upstream authority.
- [x] `specs/architecture/ash_authority_and_aeostara_conformance.md` exists.
- [x] Root and architecture docs describe Aeostara as downstream conformance layer.
- [x] Root and architecture docs define only current ASH-built authority language.

## Contracts

- [x] ASH-aligned contract set exists for observed state, intent, semantic state, diagnostics, classification, recoverability, recovery plan, fallback, containment, safe halt.
- [x] Downstream observation, intent, encoding, evidence, actuator, repair, and policy contracts are ASH-built authoritative artifacts.
- [x] Backup/rollback/verification/audit/module manifest contracts align to downstream flow.

## Algorithms

- [x] Normalization and mapping algorithms present.
- [x] Diagnosis/classification/recoverability algorithms present.
- [x] Recovery planning is recoverability-driven.
- [x] Fallback/containment/safe-halt algorithms present.
- [x] Execution/verification algorithm present.
- [x] Surface-difference evidence and actuator projection algorithms are ASH-built authoritative downstream algorithms.

## Acceptance and Traceability

- [x] `ash_conformance_targets.md` exists.
- [x] `traceability_matrix.md` exists.
- [x] `remediation_acceptance_targets.md` exists.
- [x] Acceptance scenarios cover semantic-vs-diff mismatch and escalation behavior.
- [x] `branch_alignment_targets.md` exists.

## CI Enforcement

- [x] Schema validator checks required ASH-aligned contracts.
- [x] Compliance checker validates conformance artifacts and semantic-authority gates.
- [x] Acceptance runner validates acceptance/traceability artifact completeness.
- [x] Branch alignment checker validates active branch profile invariants.
