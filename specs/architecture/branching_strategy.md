# Branching Strategy

## Branch Model

| Branch | Purpose |
|--------|---------|
| `main` | Specifications, contracts, pseudo code, architecture docs, CI scripts, test fixtures |
| `platform/windows` | Windows native implementation |
| `platform/macos` | macOS native implementation |
| `platform/ios` | iOS native implementation |

## Branch Responsibilities

### main
- JSON contract schemas
- Algorithm pseudo code
- Interface specifications
- Architecture documents
- Shared test fixtures
- CI/CD workflows (Python/YAML allowed)
- Acceptance targets
- Compliance rules

Must NOT contain:
- Compilable source code
- Platform-specific build systems
- Platform-specific UI or runtime code

### platform/* branches (native realization branches)
Platform branches are **native realization branches**. They implement shared spec behavior using their platform's native toolchain. Branch internals are not required to preserve `main`'s implementation-agnostic posture. Implementation patterns may diverge by platform.

Each platform branch contains:
- Native implementation of all contracts and algorithms
- Platform-specific build configuration and toolchain
- Platform-specific test framework and infrastructure
- Platform-specific shell/UI
- Platform manifest

## Merge Policy

```
main (specs) ──→ platform/windows
              ──→ platform/macos
              ──→ platform/ios
```

- Spec changes on `main` merge DOWN into platform branches
- Platform code NEVER merges back to `main`
- Platform branches may diverge in implementation language and patterns
- All platform branches must pass the same acceptance targets

## Release Policy

Each platform branch is independently releasable once it passes:
1. Shared acceptance targets (from `specs/acceptance/`)
2. Platform-specific build validation
3. Shipped-product compliance validation (no Python, no YAML)

## Future Repository Separation

Platform branches are planned to become separate repositories:
- `aeostara-core-spec` — evolved from `main` (specifications only)
- `aeostara-windows` — evolved from `platform/windows`
- `aeostara-macos` — evolved from `platform/macos`
- `aeostara-ios` — evolved from `platform/ios`

See [Future Repo Split Plan](future_repo_split_plan.md) for migration details. This separation is planned but not yet executed.
