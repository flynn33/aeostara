
# Rollback Lifecycle

```text
FUNCTION handle_verification_failure(context, verification_result) -> RollbackResult
  IF verification_result.status != FAILED: RETURN NOT_REQUIRED
  IF context.backupResult.status != SUCCEEDED: escalate to fallback/containment/safe halt
  restore backup by source hash
  IF restore fails: escalate monotonically and emit diagnostics
  RETURN RollbackResult
END FUNCTION
```
