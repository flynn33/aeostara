
# Policy Gate Lifecycle

```text
FUNCTION evaluate_policy_gate(plan, policy_bundle) -> PolicyDecision
  REQUIRE no mutation has occurred
  decision = deterministic_policy_rule_evaluation(plan, policy_bundle)
  IF any deny rule matches: RETURN BLOCK with diagnostics and audit
  IF any escalation rule matches: RETURN ESCALATE with diagnostics and audit
  RETURN ALLOW with diagnostics and audit
END FUNCTION
```
