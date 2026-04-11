# Verification

Post-execution verification using ASH-aligned diagnostics and state-class outcomes.

## verify_execution_outcome(recovery_plan, execution_context) -> VerificationResult

```text
FUNCTION verify_execution_outcome(recovery_plan, execution_context):
  observed = observe_system_state(execution_context.target)
  normalized = normalize_state(observed)
  mapped = map_to_ash_state(normalized, execution_context.intent)
  diagnostic = evaluate_diagnostic(mapped, ash_authority_bindings)
  state_class = classify_state(diagnostic, runtime_context())

  failed_checks = []
  IF state_class not in [STABLE, CONTAINED, SAFE_HALT]:
    failed_checks.append("unexpected post-execution state class: " + state_class)

  RETURN VerificationResult(
    success = (failed_checks is empty),
    verifiedAt = current_iso8601(),
    verificationStage = POST_EXECUTION,
    resultingSystemStateClass = state_class,
    failedChecks = failed_checks,
    ruleIDs = diagnostic.rule_ids
  )
END FUNCTION
```
