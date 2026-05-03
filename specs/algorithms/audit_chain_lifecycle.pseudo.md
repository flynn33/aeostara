
# Audit Chain Lifecycle

```text
FUNCTION append_audit_event(chain, event_type, diagnostic_reference, details) -> AuditChain
  REQUIRE diagnostic_reference.chainRootReference exists
  event.eventSequence = previous max sequence + 1
  event.diagnosticReference = diagnostic_reference
  append event
  RETURN chain
END FUNCTION
```

No lifecycle phase may complete without an audit event linked to the diagnostic chain.
