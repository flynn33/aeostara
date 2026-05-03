# Compliance Rules

## Meaning of Compliance

In this repository, compliance means downstream conformance to ASH semantic authority plus Aeostara execution-safety mechanics.

## Semantic Compliance Rules

1. ASH is upstream semantic authority.
2. Aeostara must consume ASH-derived diagnostics, classification, and recoverability semantics.
3. Diff-first artifacts cannot be semantic authority.
4. Fallback, containment, and safe-halt decisions must be explicitly represented.
5. Diagnostic artifacts must use schema/taxonomy-compatible fields.

## Execution-Safety Rules

1. Policy gates must run before mutation.
2. Backup is required before mutation execution.
3. Post-execution verification is required.
4. Rollback/escalation paths must be deterministic and auditable.
5. Audit eventing is mandatory for decision-critical actions.

## Repository Automation Rules

CI must validate:

- Presence of required conformance artifacts
- Schema validity of contract layer
- Absence of superseded drift/diff artifacts
- Acceptance and traceability artifacts present and coherent
