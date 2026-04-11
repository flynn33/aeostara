# Execution And Verification

Executes approved recovery plan steps with policy gating, backup, verification, rollback, and escalation hooks.

## execute_recovery_plan(plan, execution_context) -> VerificationResult

```text
FUNCTION execute_recovery_plan(plan, execution_context):
  enforce_policy_gate(plan, execution_context.policy)

  IF plan.requiresBackup:
    backup_ref = create_backup(execution_context)
    audit("BackupCreated", backup_ref)

  FOR EACH step IN plan.actuatorSteps:
    execute_step(step, execution_context)
    audit("ExecutionApplied", step.stepID)

  verification = verify_execution_outcome(plan, execution_context)

  IF NOT verification.success AND plan.requiresBackup:
    rollback_plan = build_rollback_plan(plan, backup_ref, verification)
    execute_rollback(rollback_plan)
    audit("RollbackExecuted", rollback_plan.rollbackPlanID)

  RETURN verification
END FUNCTION
```
