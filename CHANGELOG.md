# Changelog

All notable changes to Aeostara will be documented in this file.

## [0.5.1] - 2026-05-03

### Changed - ASH Pattern System Rebuild

- Rebuilt observation, intent, encoding, evidence, actuator, repair, policy, and fixture artifacts as current ASH Pattern System downstream specifications.
- Updated schema validation to require both ASH semantic contracts and authoritative downstream contracts.
- Updated conformance policy, acceptance targets, and branch profile checks for the rebuilt artifact surface.

## [0.5.0] - 2026-05-03

### Changed - Remediation Status

- Marked downstream ASH conformance remediation complete.
- Updated repository docs, acceptance targets, and governance policy for the completed ASH rebuild posture.

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
