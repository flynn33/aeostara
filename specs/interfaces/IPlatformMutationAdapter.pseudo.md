
# IPlatformMutationAdapter

## Purpose

Applies approved JsonMutationOperation and recovery steps after precondition, policy, backup, and verification planning gates.

## Contract Rules

- The interface is platform-neutral and specifies boundary behavior only.
- Downstream platform repos provide native implementations.
- All decisions, failures, blocked actions, and safety transitions must emit diagnostic references and audit events.
- Implementations must consume the schemas in `specs/contracts/` without changing base semantics.
