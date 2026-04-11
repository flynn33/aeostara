# IBackupProvider Interface

Backup provider for deterministic pre-mutation capture and restoration.

## Methods

### createBackup(targetReference) -> backupReference

Create a deterministic backup before mutation-capable recovery steps.

### restoreBackup(backupReference, restoreTargets) -> Boolean

Restore one or more execution targets from the specified backup reference.
