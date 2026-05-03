
# State to ASH Mapping

This algorithm is now a thin orchestration wrapper around semantic projection and ASH admissibility binding.

```text
FUNCTION map_state_to_ash(observed_system_state, desired_system_intent, projection_spec) -> MappingResult
  mapping = project_semantics(observed_system_state, desired_system_intent, projection_spec)
  IF mapping.status != MAPPED:
    RETURN mapping
  admissibility = evaluate_state_admissibility(mapping.projectedState)
  IF admissibility.status == UNCLASSIFIED:
    RETURN MappingResult(status=BLOCKED, diagnosticReferences=[admissibility.diagnosticReference])
  RETURN mapping
END FUNCTION
```

Undefined helper placeholders are not permitted; projection, confidence, and failure behavior are defined in the companion algorithms.
