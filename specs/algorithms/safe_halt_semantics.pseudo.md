
# Safe Halt Semantics

```text
FUNCTION enter_safe_halt(trigger) -> SafeHaltDecision
  diagnostic = DiagnosticEnvelope(kind=SAFE_HALT, severity=CRITICAL)
  decision.terminal = true
  decision.blockedTransitions = ["*"]
  audit(decision)
  RETURN decision
END FUNCTION

FUNCTION attempt_transition_after_safe_halt(decision, transition) -> Result
  REQUIRE decision.terminal == true
  RETURN rejected with diagnostic; no state transition occurs
END FUNCTION
```
