# Recovery Plan Generation

Generates recoverability-driven plans; low-level mutations are execution steps, not semantic authority.

## generate_recovery_plan(diagnostic, state_class, recovery_category) -> RecoveryPlan

```text
FUNCTION generate_recovery_plan(diagnostic, state_class, recovery_category):
  plan = RecoveryPlan()
  plan.recoveryPlanID = deterministic_hash(diagnostic.diagnosticID + recovery_category)
  plan.diagnosticID = diagnostic.diagnosticID
  plan.stateClass = state_class
  plan.recoveryCategory = recovery_category
  plan.requiresPolicyGate = TRUE
  plan.requiresBackup = recovery_category IN [NORMALIZE_STATE, APPLY_CORRECTION]
  plan.actuatorSteps = []

  SWITCH recovery_category:
    CASE NO_ACTION:
      plan.actuatorSteps.append(step("NO_OP", "No execution action required"))

    CASE NORMALIZE_STATE:
      plan.actuatorSteps.append(step("NORMALIZE", "Normalize state via codeword-compatible path"))
      plan.actuatorSteps.append(step("VERIFY", "Verify resulting state class is STABLE"))

    CASE APPLY_CORRECTION:
      plan.actuatorSteps.append(step("APPLY_CODEWORD_CORRECTION", "Apply deterministic correction sequence"))
      plan.actuatorSteps.append(step("VERIFY", "Verify corrected state is STABLE"))

    CASE FALLBACK_REQUIRED:
      plan.actuatorSteps.append(step("FALLBACK_SELECT", "Select fallback from canonical registry"))
      plan.actuatorSteps.append(step("VERIFY", "Verify fallback state is STABLE"))

    CASE CONTAINMENT_REQUIRED:
      plan.actuatorSteps.append(step("ENTER_CONTAINMENT", "Enter restricted operations mode"))

    CASE ESCALATION_REQUIRED:
      plan.actuatorSteps.append(step("ESCALATE", "Escalate to containment or safe-halt path"))

    CASE TERMINAL_NO_RECOVERY:
      plan.actuatorSteps.append(step("ENTER_SAFE_HALT", "Enter terminal safe-halt state"))

  END SWITCH

  plan.createdAt = current_iso8601()
  RETURN plan
END FUNCTION
```
