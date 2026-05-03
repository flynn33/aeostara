
# ASH Diagnostic Evaluation

```text
FUNCTION diagnose_mapped_state(mapping_result) -> StateValidityDiagnostic
  REQUIRE mapping_result.status == MAPPED
  admissibility = evaluate_state_admissibility(mapping_result.projectedState)
  envelope = DiagnosticEnvelope(kind=STATE_VALIDITY, ruleReferences=[ASH-STATE-VALIDITY-001])
  RETURN StateValidityDiagnostic(envelope, admissibility.status, normalizationStatus, recoverabilityCategory)
END FUNCTION
```
