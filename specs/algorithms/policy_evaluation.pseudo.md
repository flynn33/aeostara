# Policy Evaluation

Evaluates whether a recovery plan is allowed to execute, given policy constraints and diagnostics.

## evaluate_policy(recovery_plan, policy_bundle, diagnostic) -> PolicyDecision

```text
FUNCTION evaluate_policy(recovery_plan, policy_bundle, diagnostic):
  violations = []

  FOR EACH rule IN policy_bundle.rules:
    IF rule_applies(rule, recovery_plan, diagnostic) AND NOT rule_allows(rule):
      violations.append(rule.id)

  IF violations is empty:
    RETURN PolicyDecision(allowed=TRUE, reason="")

  RETURN PolicyDecision(
    allowed=FALSE,
    reason="Policy blocked execution",
    violations=violations
  )
END FUNCTION
```
