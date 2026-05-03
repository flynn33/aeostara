# Actuator Projection Planning

This is the authoritative downstream algorithm for projecting an ASH-aligned `RecoveryPlan` into deterministic Aeostara actuator mutations.

It binds repair-action planning to ASH recoverability, policy-gate, backup, execution, and verification requirements.

## to_actuator_mutations(recovery_plan, evidence) -> RepairPlanActuatorProjection

```text
FUNCTION to_actuator_mutations(recovery_plan, evidence):
  REQUIRE recovery_plan.requiresPolicyGate IS TRUE
  REQUIRE recovery_plan.requiresBackup IS TRUE

  actions = []
  FOR EACH step IN recovery_plan.actuatorSteps:
    IF step.stepType == APPLY_ACTUATOR_MUTATION:
      actions.append(RepairActionActuatorStep(
        recoveryStepID = step.stepID,
        keyPath = step.parameters.keyPath,
        actionType = step.parameters.actionType,
        fromValue = step.parameters.fromValue,
        toValue = step.parameters.toValue,
        rationale = step.description
      ))

  RETURN RepairPlanActuatorProjection(
    planID = stable_projection_id(recovery_plan.recoveryPlanID, actions),
    recoveryPlanID = recovery_plan.recoveryPlanID,
    actions = actions,
    timestamp = deterministic_plan_time(),
    requiresBackup = recovery_plan.requiresBackup,
    policyGateID = policy_gate_for(recovery_plan)
  )
END FUNCTION
```

## Authority Constraint

Actuator projections are authoritative for downstream execution. If a projection conflicts with the ASH-aligned `RecoveryPlan`, the projection must be regenerated from the recovery plan.
