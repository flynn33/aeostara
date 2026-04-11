# IAuditSink Interface

Append-only audit sink for diagnosis/recovery/escalation lifecycle records.

## Methods

### record(event)

Persist a single `AuditEvent`.

### getEvents(chainRootReference) -> List[AuditEvent]

Return audit events linked to a specific diagnostic chain root.
