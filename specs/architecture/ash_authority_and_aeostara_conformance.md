
# ASH Authority and Aeostara Conformance

ASH is the fixed upstream semantic authority. Aeostara is a platform-agnostic base design that binds ASH semantics to a JSON configuration self-healing engine.

## Non-Modification Rule

Aeostara must not modify ASH, propose ASH changes, invent ASH alternatives, extend the codeword set, redefine admissibility, or bypass ASH recovery/fallback/containment/safe-halt semantics.

## ASH Baseline

- Upstream repository: `https://github.com/flynn33/ASH-Pattern-System`
- Commit: `e123f5d7fdbb381179971f721a3292c31eb1cbc2`
- Baseline document: `ASH_BASELINE_REFERENCE.md`

## Binding Surface

Aeostara must bind all of these ASH areas:

1. `F2^9` state space.
2. Canonical 16-codeword set.
3. XOR-by-codeword transformation.
4. State admissibility.
5. State-validity diagnostics.
6. System-state classification.
7. Recoverability categories.
8. Fallback policy registry.
9. Containment and safe-halt behavior.
10. Realm identity.
11. Transition registry.
12. Topology generator.
13. Axiom evaluator.
14. Generation planning and artifact-emission materialization boundary.
15. All 5 ASH conformance categories.

## Aeostara Adaptation Layer

Aeostara may define platform-neutral JSON configuration semantics, adapter boundaries, policy gates, backup/rollback mechanics, audit contracts, and fixture outputs. Those definitions must remain subordinate to ASH whenever ASH owns the semantic question.

## Audit Requirement

Every decision, recovery step, fallback, containment, safe halt, rollback, and audit event must link to a diagnostic chain that includes ASH taxonomy-compliant rule references where ASH semantics are involved.
