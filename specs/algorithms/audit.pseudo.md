# Audit

Append-only JSON Lines audit logging for diagnosis, planning, execution, and escalation lifecycle events.

## record_audit_event(event)

```text
FUNCTION record_audit_event(event):
  line = serialize_json(event)
  append_file(audit_path(), line + "\n")
END FUNCTION
```

## make_event(event_type, subject_reference, details) -> AuditEvent

```text
FUNCTION make_event(event_type, subject_reference, details):
  RETURN AuditEvent(
    eventID = generate_uuid(),
    eventType = event_type,
    timestamp = current_iso8601(),
    subjectReference = subject_reference,
    details = details
  )
END FUNCTION
```
