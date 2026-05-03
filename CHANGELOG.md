# Changelog

All notable changes to Aeostara will be documented in this file.

## [0.5.0] - 2026-05-03

### Changed - Remediation Cleanup Complete

- Marked downstream ASH conformance remediation complete.
- Removed superseded transition contracts, helper algorithms, configuration fixtures, and superseded remediation notes from the active tree.
- Updated schema validation and branch alignment checks so removed artifacts are forbidden cleanup regressions.
- Updated conformance docs, acceptance targets, and governance policy to describe the completed cleanup posture.

## [0.4.1] - 2026-04-11

### Changed - Branch Alignment Enforcement

- Added branch alignment contract and targets.
- Added branch profile contracts for `main`, `platform_windows`, `platform_macos`, and `platform_ios`.
- Added branch-level invariant validation through `ci/branch_alignment_checker.py`.
- Updated conformance workflows for main and platform branches.

## [0.4.0] - 2026-04-11

### Changed - ASH Downstream Conformance Remediation

- Established ASH as upstream semantic authority and Aeostara as downstream conformance scope.
- Rebuilt the contract, algorithm, acceptance, traceability, and CI layers around diagnosis-first ASH conformance.
- Updated governance policy to enforce downstream ASH conformance posture.
