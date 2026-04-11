# Native Target Architecture

## Architecture Layers

1. Upstream semantic authority (ASH)
2. Downstream conformance/orchestration (Aeostara)
3. Platform-native realization (Windows/macOS/iOS)

## Aeostara Layer Responsibilities

- Observe runtime/product state
- Normalize and map to ASH-aligned state representation
- Evaluate diagnostics/classification/recoverability using ASH semantics
- Build recovery plans with deterministic gating
- Execute and verify actuator steps with backup/rollback/audit
- Escalate via fallback, containment, and safe-halt pathways

## Platform Layer Responsibilities

- Implement adapters/services using native frameworks/toolchains
- Preserve deterministic behavior and interface contracts
- Provide platform-specific observability and operations integration

## Semantic Constraint

Platform differences may change implementation details but cannot change state-class meaning, recovery category semantics, or escalation rules.
