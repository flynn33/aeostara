# Platform Status Matrix

Last updated: 2026-04-11

This matrix tracks platform realization status as product mechanics and integration readiness only.
It is not a semantic authority document.

## Semantic Authority Reminder

Semantic authority for system-state meaning and recovery semantics is ASH upstream. Platform rows below should be interpreted as implementation readiness indicators only.

## Branch Status

| Platform | Branch | Implementation Status | Build/Test Verification |
|---|---|---|---|
| Windows | `platform/windows` | Reference implementation lineage | Historical local evidence only |
| macOS | `platform/macos` | Source lineage present | Build unverified in this repo context |
| iOS | `platform/ios` | Source lineage present | Build unverified in this repo context |

## Conformance Note

Platform readiness is not equivalent to ASH conformance. ASH conformance evidence is defined in:

- `specs/acceptance/ash_conformance_targets.md`
- `specs/acceptance/traceability_matrix.md`
- `specs/acceptance/remediation_acceptance_targets.md`

## Known Gaps

1. Platform build verification lives outside this spec-focused repository scope.
2. CI proof for platform binaries is not represented here.
3. Semantic conformance must be established through acceptance and traceability artifacts, not branch status language.
