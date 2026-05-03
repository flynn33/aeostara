# Aeostara Product Boundaries

## Product Boundary

Aeostara is a downstream ASH-based healing product specification. It orchestrates product-side execution mechanics while inheriting semantic meaning from ASH.

## Upstream vs Downstream Boundary

### ASH Upstream Authority

ASH governs:

- State-space semantics
- State-validity diagnostics
- System-state classification
- Recoverability semantics
- Recovery/fallback semantics
- Containment and safe-failure semantics
- Diagnostic schema and rule taxonomy

### Aeostara Downstream Scope

Aeostara governs:

- Observation ingestion and runtime/context extraction
- Mapping and normalization of product state into ASH-evaluable input
- Policy-gated execution orchestration
- Backup/rollback/verification/audit mechanics
- Platform adapter contracts for deterministic execution

## Non-Negotiable Rules

1. Aeostara must not redefine ASH semantic classes.
2. Aeostara must not elevate diff artifacts above ASH diagnostics.
3. Aeostara may define execution mechanics only inside the ASH-aligned flow.
4. Any ambiguity is resolved in favor of ASH definitions.
