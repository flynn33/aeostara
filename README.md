# Aeostara

Aeostara is a downstream ASH-based product specification repository.

## Repository Role

This repository defines Aeostara's downstream conformance layer and product execution mechanics. Semantic authority for state validity, classification, recoverability, fallback, containment, and safe-halt behavior is inherited from the ASH Pattern System.

- Upstream semantic authority: ASH Pattern System specifications
- Downstream adaptation and execution mechanics: Aeostara
- Conflict rule: ASH wins, Aeostara changes

See [REMEDIATION_STATUS.md](REMEDIATION_STATUS.md) and [ASH Authority and Aeostara Conformance](specs/architecture/ash_authority_and_aeostara_conformance.md).

## What This Repository Contains

| Category | Location | Purpose |
|---|---|---|
| Contracts | `specs/contracts/` | ASH-aligned semantic contracts and authoritative downstream adapter/actuator/policy contracts |
| Algorithms | `specs/algorithms/` | Diagnosis-first recovery orchestration and authoritative downstream execution algorithms |
| Interfaces | `specs/interfaces/` | Execution and orchestration boundaries for platform adapters |
| Architecture | `specs/architecture/` | Authority hierarchy and downstream conformance posture |
| Acceptance | `specs/acceptance/` | ASH conformance targets, traceability, and execution model |
| Branch Profiles | `branch_profiles/` | Branch-specific alignment contracts for main/windows/macos/ios |
| Fixtures | `fixtures/` | Deterministic input scenarios for acceptance references |
| CI | `ci/` | Conformance, schema, acceptance, and branch alignment validation |

The repository contains current ASH-built contracts, algorithms, fixtures, acceptance targets, and validation gates.

## Required Decision Path

Aeostara follows this mandatory downstream flow:

`observe -> normalize -> map -> diagnose -> classify -> recoverability -> recovery-plan -> gate -> backup -> execute -> verify -> rollback/fallback/containment/safe-halt`

Surface-difference evidence and actuator projections are authoritative downstream artifacts when generated through the ASH-aligned flow.

## Branch Alignment

Branch alignment is enforced through profile contracts and CI validation:

- Branch profiles: `branch_profiles/*.profile.json`
- Contract doc: `specs/architecture/branch_alignment_contract.md`
- Validation: `python3 ci/branch_alignment_checker.py --profile <profile>`

## Boundaries

- Aeostara does not redefine ASH semantics.
- Aeostara may define and extend execution mechanics (backup, rollback, verification, policy, audit, adapters).
- Aeostara must not treat flattened observed-vs-desired drift as semantic truth.

## Compliance Meaning

In this repository, "compliance" means downstream ASH conformance, not local consistency alone.

## License

Copyright (c) 2026 James Daley. All Rights Reserved. Proprietary. See [LICENSE.md](LICENSE.md).
