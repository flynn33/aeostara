
# Recovery Plan Generation

```text
FUNCTION generate_recovery_plan(state_class, recovery_category, diagnostic) -> RecoveryPlan
  plan.stateClass = state_class
  plan.recoveryCategory = recovery_category
  plan.diagnosticReference = diagnostic.ref
  IF recovery_category == NO_ACTION:
    plan.planDisposition = NO_ACTION
    plan.recoverySteps = []
  ELSE IF recovery_category == TERMINAL_NO_RECOVERY:
    plan.planDisposition = TERMINAL
    plan.recoverySteps = generate_recovery_steps(recovery_category)
  ELSE:
    plan.planDisposition = MUTATION_REQUIRED or ESCALATION_REQUIRED according to category
    plan.recoverySteps = generate_recovery_steps(recovery_category)
  plan.planHash = recovery_plan_hash(plan)
  RETURN plan
END FUNCTION
```

`NO_ACTION` is a plan disposition with zero mutation/execution steps. No executable `NO_OP` step is valid.
