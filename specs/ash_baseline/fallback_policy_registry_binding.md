
# Fallback Policy Registry Binding

## Upstream ASH Source

- Baseline: `ASH Pattern System main@e123f5d7fdbb381179971f721a3292c31eb1cbc2`
- Source path: `specs/registries/fallback-policy-registry.md`

## Aeostara Binding Responsibility

Fallback selection traces to registry and policy; no ad hoc fallback state selection.

Aeostara records this binding through `FallbackDecision.schema.json` and the associated algorithms, fixtures, and conformance checks. Aeostara must not redefine the upstream ASH semantics behind this binding.

## Downstream Platform Obligation

Windows, Mac, and iOS repos must implement the Aeostara contract and prove expected fixture outcomes without replacing ASH semantics with platform-specific behavior.

## Diagnostics and Audit Requirements

Every rejected, ambiguous, blocked, recovered, fallback, containment, safe-halt, or materialization-boundary decision associated with this binding must emit a `DiagnosticEnvelope`, link to a `DiagnosticChain`, include taxonomy-compliant `RuleReference` entries, and be reconstructable from `AuditEvent` records.

## Conformance Tests

Required evidence is encoded in `conformance/manifest.json`, `conformance/invariant-coverage.md`, and the fixture vectors under `fixtures/conformance/`. A downstream repo must preserve expected outputs for this binding or record a deviation without changing Aeostara semantics.
