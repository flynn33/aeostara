# ASH Diagnostic Evaluation

Evaluates ASH-aligned diagnostic artifacts from mapped semantic input.

## evaluate_diagnostic(mapped_input, ash_authority_bindings) -> StateValidityDiagnostic

```text
FUNCTION evaluate_diagnostic(mapped_input, ash_authority_bindings):
  diagnostic = create_diagnostic_envelope(kind=STATE_VALIDITY, stage=DETECTION)
  diagnostic.subject_reference = mapped_input.observation_id

  IF mapped_input.mapping_status != "MAPPED":
    diagnostic.admissibility_status = UNCLASSIFIED
    diagnostic.transformation_compatibility = UNKNOWN
    diagnostic.normalization_status = BLOCKED
    diagnostic.recoverability_relevance = CONTAINMENT_NEEDED
    diagnostic.is_valid = FALSE
    diagnostic.severity = ERROR
    diagnostic.disposition = BLOCKED
    diagnostic.rule_ids = ["ASH-STATE-VALIDITY-001"]
    diagnostic.summary = "Mapping blocked before ASH evaluation"
    diagnostic.notes = [mapped_input.block_reason]
    RETURN diagnostic

  ash_result = ash_authority_bindings.evaluate(mapped_input.semantic_dimensions)

  diagnostic.admissibility_status = ash_result.admissibility_status
  diagnostic.transformation_compatibility = ash_result.transformation_compatibility
  diagnostic.normalization_status = ash_result.normalization_status
  diagnostic.recoverability_relevance = ash_result.recoverability_relevance
  diagnostic.is_valid = ash_result.is_valid
  diagnostic.severity = derive_severity(ash_result)
  diagnostic.disposition = derive_disposition(ash_result)
  diagnostic.rule_ids = ash_result.rule_ids
  diagnostic.summary = ash_result.summary
  diagnostic.notes = ash_result.notes

  RETURN diagnostic
END FUNCTION
```
