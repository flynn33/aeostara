# Branching Strategy

## Branch Model

| Branch | Purpose |
|---|---|
| `main` | Downstream conformance specs, contracts, algorithms, acceptance, CI checks |
| `platform/windows` | Windows native realization |
| `platform/macos` | macOS native realization |
| `platform/ios` | iOS native realization |

## Merge Direction

`main -> platform/*`

Platform branches do not define semantic authority back into `main`.

## Conformance Rule

All platform branches must satisfy acceptance targets and traceability obligations defined in `specs/acceptance/`.
