
# Mapping Confidence Evaluation

Projection confidence is deterministic; it never uses vague thresholds.

| Evidence condition | Result |
|---|---|
| exactly one applicable rule emits one bit | MAPPED |
| two or more applicable rules emit different bits | AMBIGUOUS |
| required source pointer is missing and no default is declared | BLOCKED |
| source value type violates binding rule | FAILED |

```text
FUNCTION evaluate_mapping_confidence(coordinate, evidence) -> ConfidenceResult
  applicable = rules_with_present_evidence(coordinate, evidence)
  IF any type violation: RETURN FAILED
  IF no applicable rule and no explicit default: RETURN BLOCKED
  IF distinct emitted bits count > 1: RETURN AMBIGUOUS
  RETURN MAPPED(bit = only emitted bit)
END FUNCTION
```
