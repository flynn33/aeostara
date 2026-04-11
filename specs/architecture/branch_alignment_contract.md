# Branch Alignment Contract

## Purpose

Define invariant alignment requirements between the downstream conformance branch and platform realization branches.

## Branch Profiles

- `main` -> `branch_profiles/main.profile.json`
- `platform/windows` -> `branch_profiles/platform_windows.profile.json`
- `platform/macos` -> `branch_profiles/platform_macos.profile.json`
- `platform/ios` -> `branch_profiles/platform_ios.profile.json`

## Alignment Invariants

1. Semantic authority language remains ASH-upstream/Aeostara-downstream on every branch.
2. Platform branches implement native mechanics without redefining semantic classes.
3. Acceptance targets remain common reference artifacts.
4. Platform branches preserve deterministic escalation semantics (fallback/containment/safe-halt).
5. Branches pass profile-aligned CI checks via `ci/branch_alignment_checker.py`.

## Validation

Branch alignment is validated per branch profile in CI and can be run locally:

`python3 ci/branch_alignment_checker.py --profile <profile>`
