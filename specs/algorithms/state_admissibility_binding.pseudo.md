
# State Admissibility Binding

```text
FUNCTION evaluate_state_admissibility(state) -> AdmissibilityResult
  IF state is not exactly 9 binary coordinates:
    RETURN UNCLASSIFIED with diagnostic
  IF state is recognized valid:
    RETURN VALID with diagnostic
  IF state is reachable through the canonical codeword orbit from a known valid state:
    RETURN TRANSFORMATION_COMPATIBLE with diagnostic
  RETURN TRANSFORMATION_INCOMPATIBLE with diagnostic
END FUNCTION
```
