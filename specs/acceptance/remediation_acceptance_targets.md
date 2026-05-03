# Remediation Acceptance Targets

These targets validate downstream ASH conformance across diagnostics, classification, recoverability, recovery planning, policy gates, fallback, containment, and safe halt.

## Required Scenarios

### Scenario 1: Diff exists but semantically stable

- Condition: observed vs intent contains superficial drift
- Expected: state class remains `STABLE`; no correction path required

### Scenario 2: Diff absent but semantically unstable

- Condition: minimal/no superficial diff, but ASH diagnostic flags instability
- Expected: state class `UNSTABLE` or `CORRECTABLE`; recovery path selected

### Scenario 3: Correction disallowed and fallback selected

- Condition: policy blocks correction or correction path unavailable
- Expected: `FALLBACK_REQUIRED`; fallback decision selected from policy registry

### Scenario 4: Fallback unavailable and containment selected

- Condition: no valid fallback candidate
- Expected: containment decision enters restricted mode

### Scenario 5: Containment exhausted and safe-halt selected

- Condition: containment breached or unresolvable blocked recovery
- Expected: safe-halt decision with terminal semantics

### Scenario 6: Verification failure after execution triggers escalation

- Condition: recovery execution completes but verification fails
- Expected: rollback and/or escalation path invoked deterministically

### Scenario 7: Policy gate blocks unsafe execution

- Condition: policy disallows planned actuator steps
- Expected: plan blocked before mutation; diagnostic and audit evidence produced

## Completion Rule

All required scenarios must be represented in acceptance targets and mapped in the traceability matrix.
