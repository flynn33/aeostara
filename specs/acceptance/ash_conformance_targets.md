# ASH Conformance Targets

## Objective

Define minimum downstream conformance targets required for Aeostara to be considered ASH-aligned.

## Target Set

1. ASH authority posture is explicit in repository architecture docs.
2. Diagnosis-first semantic flow is documented and authoritative.
3. State classification uses ASH-aligned classes.
4. Recoverability mapping is deterministic.
5. Recovery planning is recoverability-driven, not diff-first.
6. Fallback decisions are registry-driven.
7. Containment and safe-halt behaviors are explicit and terminal semantics are preserved.
8. Diagnostic artifacts are schema/taxonomy compatible.
9. Superseded drift/diff contracts, helper algorithms, and config fixtures are absent.
10. CI gates reject missing conformance artifacts and cleanup regressions.

## Minimum Evidence

Conformance evidence requires:

- Contract presence and schema validity
- Algorithm presence and semantic flow coherence
- Acceptance scenario coverage
- Traceability to ASH authority sources
- CI validation pass
