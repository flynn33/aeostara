
# Remediation Acceptance Targets

Scenario 1: observed surface drift but semantic state remains stable.
Scenario 2: no visible drift but semantic state is unstable.
Scenario 3: correction blocked; fallback selected.
Scenario 4: fallback unavailable; containment entered.
Scenario 5: containment breach; safe halt entered.
Scenario 6: verification failure triggers rollback/escalation.
Scenario 7: policy gate blocks unsafe action before mutation.

All scenarios must include diagnostics, audit expectations, and schema-valid expected outputs.
