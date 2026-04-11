# Rollback

Restores execution targets from backup when verification or policy escalation requires rollback.

## build_rollback_plan(recovery_plan, backup_ref, verification) -> RollbackPlan

```text
FUNCTION build_rollback_plan(recovery_plan, backup_ref, verification):
  RETURN RollbackPlan(
    rollbackPlanID = deterministic_hash(recovery_plan.recoveryPlanID + "rollback"),
    recoveryPlanID = recovery_plan.recoveryPlanID,
    backupReference = backup_ref,
    restoreTargets = resolve_restore_targets(recovery_plan),
    rollbackReason = join_failures(verification.failedChecks),
    createdAt = current_iso8601()
  )
END FUNCTION
```

## execute_rollback(rollback_plan) -> Boolean

```text
FUNCTION execute_rollback(rollback_plan):
  RETURN restore_from_backup(rollback_plan.backupReference, rollback_plan.restoreTargets)
END FUNCTION
```
