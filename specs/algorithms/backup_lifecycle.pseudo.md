
# Backup Lifecycle

```text
FUNCTION prepare_backup(document, plan) -> BackupResult
  IF plan.requiresBackup is false: RETURN SKIPPED with diagnostic
  sourceHash = canonical_hash(document)
  record = BackupRecord(sourceHash, storageReference)
  IF backup write fails: RETURN FAILED with escalation diagnostic
  RETURN SUCCEEDED(record)
END FUNCTION
```
