# Safe Halt Semantics

Defines terminal safe-halt decision and invariants.

## decide_safe_halt(containment_state, escalation_state) -> SafeHaltDecision

```text
FUNCTION decide_safe_halt(containment_state, escalation_state):
  decision = SafeHaltDecision()

  IF escalation_state.trigger IN [CONTAINMENT_BREACH, UNRESOLVABLE_BLOCKED_RECOVERY, OPERATOR_HALT_REQUEST, POLICY_HALT_REQUEST]:
    decision.enterSafeHalt = TRUE
    decision.trigger = escalation_state.trigger
    decision.isTerminal = TRUE
    decision.reason = escalation_state.reason
  ELSE:
    decision.enterSafeHalt = FALSE
    decision.trigger = NONE
    decision.isTerminal = FALSE
    decision.reason = "safe halt not required"

  decision.diagnosticChainReference = escalation_state.chain_root_reference
  decision.decidedAt = current_iso8601()

  RETURN decision
END FUNCTION
```

Once `enterSafeHalt = TRUE`, further transitions are forbidden.
