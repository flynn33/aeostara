# Aeostara Remediation Status

Last updated: 2026-05-03
Status: Complete - downstream ASH conformance remediation and cleanup

## Authority Statement

- ASH is the immutable upstream semantic authority.
- Aeostara is the downstream conformance and execution-spec repository.
- If Aeostara conflicts with ASH, Aeostara changes.

Aeostara preserves product execution mechanics while subordinating all semantic meaning to ASH.

## Authoritative Decision Model

Aeostara implements and documents this decision path:

`observe -> normalize -> map to ASH-aligned semantic state -> diagnose -> classify -> determine recoverability -> generate recovery plan -> gate -> backup -> execute -> verify -> rollback / fallback / containment / safe-halt`

Flattened observed-vs-intent comparison can only be used as execution evidence. It is not a semantic source of truth.

## Active Artifact Surface

The active contract surface is:

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
- Rollback, verification, audit, and module-manifest mechanics

The active algorithm surface is:

- State normalization
- State-to-ASH mapping
- ASH diagnostic evaluation
- State classification
- Recovery-category selection
- Recovery-plan generation
- Policy evaluation
- Backup, execution, verification, rollback, and audit
- Fallback, containment, and safe-halt handling

## Cleanup Result

The prior transition contracts, diff/repair helper algorithms, configuration fixtures, and superseded remediation notes have been removed from the active repository tree.

CI now treats those files as forbidden cleanup regressions rather than required marked artifacts.

## Branch Alignment

Branch alignment remains part of conformance scope.

- Profiles define required branch invariants: `branch_profiles/*.profile.json`
- Contract authority: `specs/architecture/branch_alignment_contract.md`
- Acceptance target: `specs/acceptance/branch_alignment_targets.md`
- Automation enforcement: `ci/branch_alignment_checker.py` and `.github/workflows/*`

## Completed Phases

- Phase 0 Control/Freeze: complete
- Phase 1 Architecture authority reset: complete
- Phase 2-6 Contracts and algorithms: complete
- Phase 7 Acceptance rebuild: complete
- Phase 8 CI hardening: complete
- Phase 9 Cleanup: complete

## Acceptance Gate

Remediation is complete because:

1. ASH is explicit upstream authority in repo docs.
2. Diff-first semantics are not authoritative.
3. Required ASH-aligned contracts and algorithms exist.
4. Acceptance artifacts and traceability matrix cover ASH conformance scenarios.
5. CI scripts enforce required downstream conformance artifacts and reject cleanup regressions.
6. Branch profile checks pass for each active branch profile represented in this repository.
