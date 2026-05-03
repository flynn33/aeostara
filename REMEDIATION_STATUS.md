# Aeostara Remediation Status

Last updated: 2026-05-03
Status: Complete - downstream rebuild under the ASH Pattern System

## Authority Statement

- ASH is the immutable upstream semantic authority.
- Aeostara is the downstream conformance and execution-spec repository.
- If Aeostara conflicts with ASH, Aeostara changes.

Aeostara defines authoritative downstream contracts, algorithms, fixtures, and execution mechanics built on the ASH Pattern System.

## Authoritative Decision Model

Aeostara implements and documents this decision path:

`observe -> normalize -> map to ASH-aligned semantic state -> diagnose -> classify -> determine recoverability -> generate recovery plan -> gate -> backup -> execute -> verify -> rollback / fallback / containment / safe-halt`

Surface-difference evidence and actuator projections are valid only inside this ASH-aligned flow.

## Active Contract Surface

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
- Observation, intent, encoding, evidence, actuator, repair, and policy contracts built as downstream ASH artifacts

## Active Algorithm Surface

- State normalization
- State-to-ASH mapping
- ASH diagnostic evaluation
- State classification
- Recovery-category selection
- Recovery-plan generation
- Surface-difference evidence
- Actuator projection planning
- Policy evaluation
- Backup, execution, verification, rollback, and audit
- Fallback, containment, and safe-halt handling

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
- Phase 9 Cleanup and ASH rebuild: complete

## Acceptance Gate

Remediation is complete because:

1. ASH is explicit upstream authority in repo docs.
2. Aeostara artifacts are rebuilt as current ASH Pattern System downstream specifications.
3. Required ASH-aligned contracts and algorithms exist.
4. Acceptance artifacts and traceability matrix cover ASH conformance scenarios.
5. CI scripts enforce required downstream conformance artifacts.
6. Branch profile checks pass for each active branch profile represented in this repository.
