
# Recovery Blocked Path Escalation

```text
FUNCTION escalate_blocked_recovery(category, reason) -> EscalationDecision
  CASE NORMALIZE_STATE -> CONTAINMENT_REQUIRED when normalization path is not computable
  CASE APPLY_CORRECTION -> FALLBACK_REQUIRED when correction is ambiguous or blocked
  CASE FALLBACK_REQUIRED -> CONTAINMENT_REQUIRED when registry has no candidate
  CASE CONTAINMENT_REQUIRED -> TERMINAL_NO_RECOVERY when boundary is breached
  CASE ESCALATION_REQUIRED -> TERMINAL_NO_RECOVERY when no authority is reachable
END FUNCTION
```

Escalation is monotonic and always emits diagnostics and audit events.
