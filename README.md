
# Aeostara

Aeostara is a platform-agnostic base-design specification package for a self-healing JSON configuration engine. It conforms to the ASH Pattern System and instructs downstream Windows, macOS, and iOS implementation repositories.

## Repository Role

Aeostara is platform-agnostic. ASH is the fixed upstream semantic authority. Platform repos consume Aeostara; Aeostara does not depend on platform repositories or native platform source code to be base-design complete.

```text
ASH Pattern System
        ↓
Aeostara platform-agnostic base design
        ↓
flynn33/Aeostara-Windows
flynn33/Aeostara-Mac-iOS
```

Conflict rule: ASH wins, Aeostara changes. This repository must not modify ASH, propose ASH changes, or add native Windows, Mac, or iOS implementation source.

See [BASE_DESIGN_COMPLETION.md](BASE_DESIGN_COMPLETION.md), [ASH_BASELINE_REFERENCE.md](ASH_BASELINE_REFERENCE.md), [Repository Role Contract](specs/architecture/repository_role_contract.md), and [Repository Separation Status](REPOSITORY_SEPARATION_STATUS.md).

## What This Repository Contains

| Category | Location | Purpose |
|---|---|---|
| ASH baseline bindings | `specs/ash_baseline/` | Aeostara bindings to the fixed ASH source areas and invariant categories |
| Contracts | `specs/contracts/` | Platform-neutral JSON schemas for every lifecycle boundary object |
| Algorithms | `specs/algorithms/` | Diagnosis-first, JSON Pointer based, ASH-aligned pseudocode |
| Interfaces | `specs/interfaces/` | Platform-neutral adapter and orchestration boundaries |
| Architecture | `specs/architecture/` | Authority hierarchy, base/platform boundary, and versioning rules |
| Acceptance | `specs/acceptance/` | Base-design completion gates, ASH traceability, and downstream handoff acceptance |
| Conformance | `conformance/` | Module mapping, invariant coverage, diagnostics, materialization boundary, deviations, and judgment artifacts |
| Fixtures | `fixtures/conformance/` and `fixtures/schema_examples/` | Expected-output vectors and valid schema instances |
| CI | `ci/` | Schema, fixture, traceability, JSON semantics, diagnostic-chain, recovery, and handoff validators |
| Downstream handoff | `implementation_handoff/` and `templates/platform_repo/` | Requirements and templates for Windows, macOS, and iOS repos |

## Downstream Repositories

| Product surface | Repository | Permanent branch |
|---|---|---|
| Windows realization | `flynn33/Aeostara-Windows` | `main` |
| macOS realization | `flynn33/Aeostara-Mac-iOS` | `platform/macos` |
| iOS realization | `flynn33/Aeostara-Mac-iOS` | `platform/ios` |
| Apple repository coordination | `flynn33/Aeostara-Mac-iOS` | `main` |

## Required Decision Path

Aeostara defines this mandatory platform-neutral lifecycle:

`observe -> normalize -> project JSON/configuration state -> bind to ASH -> diagnose -> classify -> determine recoverability -> generate recovery plan -> evaluate policy gate -> prepare backup -> execute approved plan -> verify -> rollback/fallback/containment/safe-halt -> emit diagnostic and audit chain`

Surface differences are evidence only. Generic JSON diffing is not semantic truth. Recovery is derived from diagnosis, classification, and recoverability, not from CRUD repair operations.

## Completion Meaning

Aeostara base design is complete only when a Windows, macOS, or iOS implementation team can implement Aeostara faithfully from this repository without inventing base semantics, recovery logic, JSON semantics, diagnostics, audit requirements, or conformance expectations.

Base-design completion does not require platform-native source files. Platform-specific implementation work belongs in downstream repositories.

## Validation

Run the full base-design gate locally:

```text
python3 -m pip install -r ci/requirements.txt
python3 ci/conformance_runner.py .
```

Key component gates are also runnable individually:

```text
python3 ci/validate_schemas.py .
python3 ci/schema_instance_validator.py .
python3 ci/fixture_validator.py .
python3 ci/interface_contract_checker.py .
python3 ci/algorithm_completeness_checker.py .
python3 ci/lifecycle_execution_checker.py .
python3 ci/traceability_checker.py .
python3 ci/ash_invariant_checker.py .
python3 ci/json_semantics_checker.py .
python3 ci/diagnostic_chain_checker.py .
python3 ci/recovery_consistency_checker.py .
python3 ci/downstream_handoff_checker.py .
python3 ci/base_design_completion_checker.py .
python3 ci/workflow_integrity_checker.py .
python3 ci/acceptance_runner.py .
python3 ci/compliance_checker.py .
python3 ci/release_readiness_checker.py .
python3 ci/repository_separation_checker.py . --read-only --online
python3 ci/program_closeout_runner.py . --online
```

## Contributing

This project is open source under Apache License, Version 2.0. You are welcome to use, modify, and redistribute the code under that license.

Outside contributions to this repository are not accepted. Pull requests and collaboration requests will not be reviewed or merged. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Copyright 2026 James Daley

This project is licensed under the Apache License, Version 2.0.
See the [LICENSE](LICENSE) file for the full terms.
