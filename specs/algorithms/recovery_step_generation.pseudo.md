
# Recovery Step Generation

```text
FUNCTION generate_recovery_steps(category) -> List[RecoveryStep]
  SWITCH category
    CASE NO_ACTION: RETURN []
    CASE NORMALIZE_STATE: RETURN [RecoveryStep(stepType=NORMALIZE_STATE)]
    CASE APPLY_CORRECTION: RETURN [RecoveryStep(stepType=APPLY_CORRECTION), RecoveryStep(stepType=VERIFY)]
    CASE FALLBACK_REQUIRED: RETURN [RecoveryStep(stepType=SELECT_FALLBACK), RecoveryStep(stepType=VERIFY)]
    CASE CONTAINMENT_REQUIRED: RETURN [RecoveryStep(stepType=ENTER_CONTAINMENT)]
    CASE ESCALATION_REQUIRED: RETURN [RecoveryStep(stepType=ESCALATE)]
    CASE TERMINAL_NO_RECOVERY: RETURN [RecoveryStep(stepType=ENTER_SAFE_HALT)]
END FUNCTION
```

There is no executable NO_OP step. `NO_ACTION` is represented as plan disposition with zero mutation steps.
