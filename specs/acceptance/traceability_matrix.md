# Traceability Matrix

| Behavior | ASH Authority Source | Aeostara Adaptation Artifact | Acceptance Target |
|---|---|---|---|
| State validity diagnostics | `specs/core/state-validity-diagnostics.pseudo.md` | `specs/contracts/StateValidityDiagnostic.schema.json`, `specs/algorithms/ash_diagnostic_evaluation.pseudo.md` | Scenario 1, 2 |
| System-state classification | `specs/core/system-state-classification.pseudo.md` | `specs/contracts/SystemStateClass.schema.json`, `specs/algorithms/state_classification.pseudo.md` | Scenario 1, 2 |
| Recoverability mapping | `specs/core/recoverability-semantics.pseudo.md` | `specs/contracts/RecoveryCategory.schema.json`, `specs/algorithms/recovery_category_selection.pseudo.md` | Scenario 2, 3 |
| Recovery planning semantics | `specs/algorithms/recovery-fallback-semantics.pseudo.md` | `specs/contracts/RecoveryPlan.schema.json`, `specs/algorithms/recovery_plan_generation.pseudo.md` | Scenario 3, 6 |
| Fallback policy behavior | `specs/registries/fallback-policy-registry.md` | `specs/contracts/FallbackDecision.schema.json`, `specs/algorithms/fallback_selection.pseudo.md` | Scenario 3, 4 |
| Containment behavior | `specs/algorithms/containment-safe-failure-semantics.pseudo.md` | `specs/contracts/ContainmentDecision.schema.json`, `specs/algorithms/containment_mode.pseudo.md` | Scenario 4, 5 |
| Safe-halt terminal behavior | `specs/algorithms/containment-safe-failure-semantics.pseudo.md` | `specs/contracts/SafeHaltDecision.schema.json`, `specs/algorithms/safe_halt_semantics.pseudo.md` | Scenario 5 |
| Execution + verification + rollback | `specs/algorithms/recovery-fallback-semantics.pseudo.md` | `specs/algorithms/execution_and_verification.pseudo.md`, `specs/contracts/VerificationResult.schema.json`, `specs/contracts/RollbackPlan.schema.json` | Scenario 6 |
| Diagnostic schema/taxonomy conformity | `specs/interfaces/diagnostic-schema.md`, `specs/interfaces/rule-id-taxonomy.md` | `specs/contracts/StateValidityDiagnostic.schema.json` | Scenario 1-7 |
