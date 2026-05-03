
# Traceability Matrix

| Lifecycle area | Contract | Algorithm | Fixture evidence |
|---|---|---|---|
| Observation | ObservedSystemState | healing_flow | end_to_end_healing_vectors |
| Desired intent | DesiredSystemIntent | healing_flow | end_to_end_healing_vectors |
| JSON semantics | JsonPointer, JsonMutationOperation | json_pointer_operations, mutation_precondition_check | json_semantics_vectors |
| Semantic projection | SemanticProjectionSpec, MappingResult | semantic_projection | semantic_projection_vectors |
| ASH state | AshState, AshSemanticState | state_to_ash_mapping | ash_codeword_vectors |
| Diagnostics | StateValidityDiagnostic, DiagnosticEnvelope, DiagnosticChain | diagnostic_chain_integrity | diagnostic_chain_vectors |
| Classification | SystemStateClass | state_classification | state_admissibility_vectors |
| Recovery | RecoveryCategory, RecoveryPlan, RecoveryStep | recovery_plan_generation | recovery_escalation_vectors |
| Fallback | FallbackDecision | fallback_selection | recovery_escalation_vectors |
| Containment | ContainmentDecision | containment_mode | safe_halt_terminal_vectors |
| Safe halt | SafeHaltDecision | safe_halt_semantics | safe_halt_terminal_vectors |
| Policy | PolicyBundle, PolicyDecision | policy_gate_lifecycle | policy_block_vectors |
| Backup/rollback | BackupRecord, BackupResult, RollbackResult | backup_lifecycle, rollback_lifecycle | backup_rollback_vectors |
| Verification | VerificationPlan, VerificationResult | verification_plan_generation | backup_rollback_vectors |
| Audit | AuditEvent, AuditChain | audit_chain_lifecycle | diagnostic_chain_vectors |
