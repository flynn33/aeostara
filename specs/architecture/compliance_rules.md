# Compliance Rules

## Shipped Product Rules

1. **Native only** — shipped product must be a native compiled binary
2. **No Python** — shipped product must not depend on Python runtime
3. **No YAML** — shipped product must not include a YAML parser
4. **JSON-only v0.1** — all configuration files are JSON
5. **Code-agnostic specs** — shared behavior definitions on `main` remain code-agnostic; platform branches are native realization branches and may adopt platform-specific patterns
6. **Forsetti boundary compliance** — platform branches may integrate with their platform's Forsetti framework while observing boundary rules: no framework modification, no direct module-to-module communication, no direct OS communication, no module-owned UI, framework-mediated I/O only

## Repository Automation (Exempt)

Python and YAML are permitted in:
- GitHub Actions workflows (`.github/workflows/`)
- CI scripts (`ci/`)
- Repository automation scripts (`.github/scripts/`)

These are not part of the shipped product.

## Per-Platform Rules

Platform-specific compliance rules (toolchain choices, build flags, framework dependencies, test frameworks) are the responsibility of each platform implementation. They are not prescribed by this authority repository.

Each platform implementation must satisfy:
1. The shipped product rules above
2. The acceptance targets in `specs/acceptance/acceptance_targets.md`
3. Forsetti boundary compliance (rule 6 above)

Platform-specific compliance documentation will reside in future platform repositories. See [Future Repo Split Plan](future_repo_split_plan.md).
