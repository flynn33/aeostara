
# State Classification

```text
FUNCTION classify_system_state(diagnostic, context) -> SystemStateClass
  IF context.safeHalt == true: RETURN SAFE_HALT
  IF context.contained == true: RETURN CONTAINED
  IF diagnostic.admissibilityStatus == VALID AND diagnostic.normalizationStatus == ALREADY_VALID: RETURN STABLE
  IF diagnostic.admissibilityStatus == TRANSFORMATION_COMPATIBLE AND diagnostic.normalizationStatus == NORMALIZABLE: RETURN CORRECTABLE
  IF diagnostic.admissibilityStatus == TRANSFORMATION_INCOMPATIBLE: RETURN DEGRADED
  RETURN FAILED
END FUNCTION
```
