# Aeostara Remediation Status

Last updated: 2026-04-11
Status: In-progress major remediation to downstream ASH conformance

## Authority Statement

- ASH is the immutable upstream semantic authority.
- Aeostara is the sole remediation target.
- If Aeostara conflicts with ASH, Aeostara changes.

Aeostara is now positioned as a downstream ASH-based product-spec repository that preserves product execution mechanics while replacing legacy semantic authority.

## Target Decision Model

Aeostara must implement and document this decision path:

`observe -> normalize -> map to ASH-aligned semantic state -> diagnose -> classify -> determine recoverability -> generate recovery plan -> gate -> backup -> execute -> verify -> rollback / fallback / containment / safe-halt`

The legacy path is non-authoritative:

`flatten state -> diff keys -> emit Set/Add/Remove -> execute`

## Artifact Classes

### Preserve (mechanics only)

- Backup mechanics
- Rollback mechanics
- Verification mechanics
- Audit mechanics
- Policy-gate mechanics
- Deterministic execution discipline
- Platform adapter framing

These remain subordinate helpers and must not define semantic truth.

### Rewrite

- Root and architecture docs that claimed Aeostara-owned healing semantics
- Acceptance and compliance documents
- Interface contracts that accepted generic drift-first artifacts
- CI/compliance scripts to enforce ASH downstream conformance

### Replace

- Legacy drift-first semantic contracts (`ObservedState`, `DesiredState`, `EncodedState`, `DriftEvent`, `RepairAction`, `RepairPlan`, `Invariant`) with ASH-aligned contract layer
- Drift-first algorithms (`drift_analysis`, `repair_planning`, `healing_flow`) with diagnosis/classification/recoverability-first semantics

### Remove from authority

Legacy files are retained only as historical or helper references. They are explicitly marked non-authoritative and cannot be used as the semantic source of truth.

## Branch Alignment Remediation

Branch alignment is now part of remediation scope.

- Profiles define required branch invariants: `branch_profiles/*.profile.json`
- Contract authority: `specs/architecture/branch_alignment_contract.md`
- Acceptance target: `specs/acceptance/branch_alignment_targets.md`
- Automation enforcement: `ci/branch_alignment_checker.py` and `.github/workflows/*`

This workspace currently contains no local git branch checkouts. Direct branch code edits require branch worktrees or branch repositories to be available in workspace.

## Minimum Required Conformance Surface

Aeostara must expose downstream artifacts for:

- Observed system state
- Desired system intent
- ASH semantic state
- State-validity diagnostics
- System-state classification
- Recovery-category selection
- Recovery plan
- Fallback decision
- Containment decision
- Safe-halt decision

## Progress Snapshot

- Phase 0 Control/Feeze: complete in documentation
- Phase 1 Architecture authority reset: complete in documentation
- Phase 2-6 contracts and algorithms: complete in repository specifications
- Phase 7 acceptance rebuild: complete in repository specifications
- Phase 8 CI hardening: complete in repository automation scripts
- Branch alignment framework and CI profiles: complete
- Phase 9 cleanup: active and continuous

## Legacy Marking Policy

Legacy files are retained only when useful for helper mechanics or historical traceability, and must include explicit deprecation markers and non-authoritative status.

## Acceptance Gate

Remediation is considered complete only when:

1. ASH is explicit upstream authority in repo docs.
2. Legacy diff-first semantics are not authoritative.
3. Required ASH-aligned contracts and algorithms exist.
4. Acceptance artifacts and traceability matrix cover ASH conformance scenarios.
5. CI scripts enforce required downstream conformance artifacts and reject legacy-authority regressions.
6. Branch profile checks pass for each active branch.
