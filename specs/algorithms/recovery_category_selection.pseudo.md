# Recovery Category Selection

Maps state class to deterministic recovery category.

## select_recovery_category(system_state_class) -> RecoveryCategory

```text
FUNCTION select_recovery_category(system_state_class):
  SWITCH system_state_class:
    CASE STABLE:     RETURN NO_ACTION
    CASE UNSTABLE:   RETURN NORMALIZE_STATE
    CASE CORRECTABLE: RETURN APPLY_CORRECTION
    CASE DEGRADED:   RETURN FALLBACK_REQUIRED
    CASE CONTAINED:  RETURN CONTAINMENT_REQUIRED
    CASE FAILED:     RETURN ESCALATION_REQUIRED
    CASE SAFE_HALT:  RETURN TERMINAL_NO_RECOVERY
  END SWITCH
END FUNCTION
```

Blocked paths must escalate to a more severe category; never de-escalate silently.
