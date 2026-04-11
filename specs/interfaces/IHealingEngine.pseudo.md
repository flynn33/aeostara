# IHealingEngine Interface

Top-level downstream orchestration interface. Semantic authority is ASH; this interface exposes execution orchestration mechanics.

## Methods

### evaluate(observationSource, intentSource) -> EvaluationResult

Runs observe/normalize/map/diagnose/classify/recoverability selection without applying mutation.

**Returns:**
- `diagnostic` (StateValidityDiagnostic)
- `systemStateClass` (SystemStateClass)
- `recoveryCategory` (RecoveryCategory)
- `proposedRecoveryPlan` (RecoveryPlan)

### heal(observationSource, intentSource, policySource, auditSink) -> HealResult

Executes the full diagnosis-first flow with policy, backup, verification, rollback/fallback/containment/safe-halt handling.

**Returns:**
- `success` (boolean)
- `terminal` (boolean)
- `executedPlan` (RecoveryPlan)
- `verification` (VerificationResult)
- `fallbackDecision` (FallbackDecision, optional)
- `containmentDecision` (ContainmentDecision, optional)
- `safeHaltDecision` (SafeHaltDecision, optional)
- `auditEvents` (list of AuditEvent)
- `message` (string)

### dryRunRecovery(observationSource, intentSource, policySource) -> DryRunResult

Evaluates and plans recovery without mutating targets.
