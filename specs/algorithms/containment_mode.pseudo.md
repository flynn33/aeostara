# Containment Mode

Defines deterministic containment entry and restricted operations handling.

## decide_containment(recovery_outcome, policy_context) -> ContainmentDecision

```text
FUNCTION decide_containment(recovery_outcome, policy_context):
  decision = ContainmentDecision()

  IF recovery_outcome.requires_containment:
    decision.enterContainment = TRUE
    decision.trigger = recovery_outcome.trigger
    decision.restrictedOperations = policy_context.restricted_operations_profile
    decision.awaitingResolution = TRUE
    decision.reason = recovery_outcome.reason
  ELSE:
    decision.enterContainment = FALSE
    decision.trigger = NONE
    decision.restrictedOperations = []
    decision.awaitingResolution = FALSE
    decision.reason = "containment not required"

  decision.decidedAt = current_iso8601()
  RETURN decision
END FUNCTION
```
