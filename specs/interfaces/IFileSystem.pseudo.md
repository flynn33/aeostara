# IFileSystem

## Single Responsibility

Abstracts platform-neutral byte and file operations used by downstream adapters.

## Consumed Contract Types

`PATH`, `BYTE_SEQUENCE`

## Produced Contract Types

`BYTE_SEQUENCE`, `OPERATION_RESULT`, `boolean`, `SHA256_HEX`

## Operations

- `read(path: PATH) -> BYTE_SEQUENCE`
- `writeAtomically(path: PATH, bytes: BYTE_SEQUENCE) -> OPERATION_RESULT`
- `appendAtomically(path: PATH, bytes: BYTE_SEQUENCE) -> OPERATION_RESULT`
- `copyAtomically(source: PATH, destination: PATH) -> OPERATION_RESULT`
- `exists(path: PATH) -> boolean`
- `computeSHA256(path: PATH) -> SHA256_HEX`

## Preconditions

- Inputs must conform to the named contract schemas before the operation begins.
- Referenced diagnostic, audit, policy, backup, and recovery identifiers must be resolvable within the active lifecycle context when supplied.
- Operations that can lead to mutation require completed planning, policy, backup, and precondition evidence before execution.

## Postconditions

- The returned contract object is schema-valid and semantically consistent with the operation outcome.
- Every blocked, failed, ambiguous, or terminal result has a linked `DiagnosticReference`.
- State-changing operations preserve enough evidence for audit-chain reconstruction and rollback decisions.

## Side-Effect Classification

read-only for read, exists, and computeSHA256; persistence for atomic write, append, and copy.

## Determinism Requirements

- Equivalent inputs produce equivalent contract outputs, deterministic ordering, deterministic identifiers where the governing algorithm defines them, and stable SHA-256 hashes for canonical JSON content.
- Ambiguous or missing evidence is reported as `BLOCKED`, `AMBIGUOUS`, or `FAILED`; it is never coerced into a successful value.

## DiagnosticEnvelope and DiagnosticChain Obligations

- Each operation emits or propagates a `DiagnosticEnvelope` for material decisions and failures.
- Diagnostic chain roots, parent links, rule references, and source references must be valid and reconstructable.
- Invalid policy, missing evidence, failed persistence, failed preconditions, and adapter errors fail closed.

## AuditEvent and AuditChain Obligations

- Lifecycle operations append ordered `AuditEvent` records for completed phases and terminal failures.
- Event sequence numbers are one-based and contiguous.
- Audit persistence failure is itself a lifecycle failure and cannot be converted to success.

## Blocked and Failure Behavior

- Blocked inputs return the contract result specified by the lifecycle algorithm with mutation disabled unless a prior approved rollback operation is in progress.
- Failures preserve diagnostic context, prevent silent fallback, and select rollback, fallback, containment, or safe halt only through the fixed escalation algorithms.
- No operation may fabricate empty state, empty policy, empty diagnostics, or success on exception.

## Downstream Swift Protocol Mapping Rule

Downstream Swift implementations map this interface to a protocol with the same operation names, value-semantic DTOs matching the contract schemas, explicit throwing or result-return failure channels, and no platform semantic substitution.

## Downstream C++ Pure-Virtual Mapping Rule

Downstream C++ implementations map this interface to a pure-virtual boundary with the same operation names, contract DTOs matching the schemas, explicit error results, and no ownership model that hides failed diagnostics or audit persistence.

## Verification Cases

- Valid input returns a schema-valid produced contract with linked diagnostics.
- Missing required input fails closed with no unauthorized mutation.
- Ambiguous evidence remains ambiguous and blocks success.
- Policy, backup, execution, verification, rollback, fallback, containment, and safe-halt failures follow the fixed lifecycle where applicable.
- Repeated execution with identical immutable inputs is deterministic.

## Prohibited Behavior

- Do not mutate during planning or dry-run paths.
- Do not invent contract fields, enum values, lifecycle phases, ASH coordinates, or JSON addressing rules.
- Do not merge platform-native implementation source into agnostic `main`.
- Do not suppress diagnostics, audit failures, backup failures, policy failures, or verification failures.
