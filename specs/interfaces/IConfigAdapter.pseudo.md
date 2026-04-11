# IConfigAdapter Interface

Adapter boundary for collecting observed system state and applying execution steps. This interface does not define semantic truth.

## Methods

### observeSystemState(source) -> ObservedSystemState

Collect runtime/product state from adapter-specific sources.

### normalizeInput(observed) -> object

Produce deterministic normalized input for state-to-ASH mapping.

### applyActuatorSteps(target, steps) -> Boolean

Apply execution-level actuator steps produced by `RecoveryPlan`.

### snapshotTarget(target) -> string

Create adapter-level snapshot reference used by backup/rollback flow.

### restoreSnapshot(snapshotRef, target) -> Boolean

Restore a target from a snapshot reference.
