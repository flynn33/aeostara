# Healing Flow (ASH-Aligned)

End-to-end diagnosis-first orchestration for downstream Aeostara execution.

## heal(observation_source, intent_source, policy_source) -> HealResult

```text
FUNCTION heal(observation_source, intent_source, policy_source):
  observed = observe_system_state(observation_source)
  intent = load_desired_intent(intent_source)

  normalized = normalize_state(observed)
  mapped = map_to_ash_state(normalized, intent)

  diagnostic = evaluate_diagnostic(mapped, ash_authority_bindings)
  state_class = classify_state(diagnostic, runtime_context())
  recovery_category = select_recovery_category(state_class)
  plan = generate_recovery_plan(diagnostic, state_class, recovery_category)

  policy_decision = evaluate_policy(plan, policy_source, diagnostic)
  IF NOT policy_decision.allowed:
    RETURN blocked_result(policy_decision)

  verification = execute_recovery_plan(plan, execution_context())

  IF verification.success:
    RETURN success_result(plan, verification)

  fallback = select_fallback(diagnostic, fallback_registry())
  IF fallback.selectionOutcome == SELECTED:
    fallback_verification = execute_fallback(fallback)
    IF fallback_verification.success:
      RETURN success_via_fallback_result(plan, fallback, fallback_verification)

  containment = decide_containment(recovery_outcome_from(verification, fallback), policy_context())
  IF containment.enterContainment:
    safe_halt = decide_safe_halt(containment_state(), escalation_state())
    IF safe_halt.enterSafeHalt:
      RETURN terminal_result(plan, containment, safe_halt)
    RETURN contained_result(plan, containment)

  RETURN failure_result(plan, verification)
END FUNCTION
```
