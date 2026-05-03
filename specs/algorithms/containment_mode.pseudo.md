
# Containment Mode

```text
FUNCTION enter_containment(trigger, boundary) -> ContainmentDecision
  diagnostic = DiagnosticEnvelope(kind=CONTAINMENT, severity=CRITICAL)
  decision = ContainmentDecision(boundary, allowedOperations, restrictedOperations, diagnostic)
  audit(decision)
  RETURN decision
END FUNCTION

FUNCTION evaluate_containment_breach(decision, attempted_operation) -> EscalationDecision
  IF attempted_operation in decision.restrictedOperations:
    RETURN escalate to TERMINAL_NO_RECOVERY with diagnostic
END FUNCTION
```
