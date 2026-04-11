# Backup

Creates deterministic backup artifacts before execution of mutation-capable steps.

## create_backup(execution_context) -> backup_reference

```text
FUNCTION create_backup(execution_context):
  timestamp = current_timestamp("YYYYMMDD_HHmmss")
  backup_reference = execution_context.target + ".backup." + timestamp
  success = file_copy(execution_context.target, backup_reference)
  IF NOT success:
    ERROR "backup creation failed"
  RETURN backup_reference
END FUNCTION
```
