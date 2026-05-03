
# IHealingEngine

## Purpose

Coordinates observe, normalize, project, diagnose, plan, policy, backup, execute, verify, rollback, fallback, containment, safe halt, diagnostics, and audit.

## Contract Rules

- The interface is platform-neutral and specifies boundary behavior only.
- Downstream platform repos provide native implementations.
- All decisions, failures, blocked actions, and safety transitions must emit diagnostic references and audit events.
- Implementations must consume the schemas in `specs/contracts/` without changing base semantics.
