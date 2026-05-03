
# Execution Step Lifecycle

```text
FUNCTION execute_steps(context, steps) -> List[ExecutionStepResult]
  REQUIRE context.policyDecision.decision == ALLOW
  REQUIRE context.verificationPlan.generatedBeforeMutation == true
  FOR step IN steps:
    precondition = check all mutation preconditions
    IF precondition blocked: record BLOCKED diagnostic and stop
    execute platform-neutral step through adapter boundary
    record ExecutionStepResult and audit event
  RETURN results
END FUNCTION
```
