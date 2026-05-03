
# Healing Flow

```text
FUNCTION heal(observed_document, desired_document, policy_bundle) -> HealResult
  observed = observe(observed_document)
  desired = build_desired_intent(desired_document)
  normalized = normalize_json_inputs(observed, desired)
  mapping = project_semantics(normalized.observed, normalized.desired, projection_spec)
  diagnostic = diagnose mapped ASH state
  state_class = classify_system_state(diagnostic)
  recovery_category = classify_recoverability(state_class)
  plan = generate_recovery_plan(state_class, recovery_category, diagnostic)
  IF plan.planDisposition == NO_ACTION:
    RETURN HealResult(status=NO_ACTION, auditChain, diagnosticChain)
  policy_decision = evaluate_policy_gate(plan, policy_bundle)
  IF policy_decision.decision != ALLOW:
    RETURN blocked or escalated result with diagnostics and audit
  verification_plan = generate_verification_plan(mapping.projectedState, plan)
  backup_result = prepare_backup(observed_document, plan)
  execution_results = execute_steps(context, plan.recoverySteps)
  verification_result = verify(verification_plan)
  IF verification_result.status == FAILED:
    rollback_result = handle_verification_failure(context, verification_result)
    apply fallback/containment/safe halt escalation if needed
  RETURN HealResult with diagnosticChain and auditChain
END FUNCTION
```
