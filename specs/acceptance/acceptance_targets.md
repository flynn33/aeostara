# Acceptance Targets

All platform implementations must pass these scenarios to be considered compliant.

## Shared Behavior Scenarios

### 1. Valid Config — No Drift
**Input:** `fixtures/valid_config.json` + `fixtures/desired_state.json`
**Expected:** validate returns valid=true, no drifts, exit code 0

### 2. Invalid Config — Parse Error
**Input:** `fixtures/invalid_config.json` (malformed JSON)
**Expected:** validate returns valid=false, error message, exit code 2

### 3. Policy Block — Critical Invariant Violation
**Input:** `fixtures/policy_blocked_config.json` + `fixtures/desired_state.json` + `fixtures/invariants.json`
**Expected:** heal returns blocked, audit event with type=PolicyBlocked, exit code 1

### 4. Successful Repair
**Input:** `fixtures/repairable_config.json` + `fixtures/desired_state.json` + `fixtures/invariants.json`
**Expected:** heal returns success=true, backup created, config repaired, audit trail, exit code 0

### 5. Forced Rollback — Verification Failure
**Input:** repairable config with a mock/stub file system that returns bad content on verify re-read
**Expected:** rollback executed, audit records VerificationFailed + RollbackExecuted

> **Execution method:** This scenario requires fault injection into the verify/rollback path via a mock or stub file system. It cannot be verified through black-box CLI invocation alone and must be proven in each platform's native test infrastructure. See [Acceptance Execution Model](acceptance_execution_model.md).

## Cross-Platform Acceptance

1. Root specifications remain correct (schemas validate, pseudo code is consistent)
2. Each platform implementation passes all 5 shared behavior scenarios
3. Deterministic outputs match across platforms for the same input

## Compliance Acceptance

1. Shipped product does not require Python
2. Shipped product does not require YAML
3. Core implementation remains host-agnostic
4. Forsetti bridges are isolated from core healing modules
