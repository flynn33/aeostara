# State Classification

Classifies system state from ASH diagnostic output using deterministic ASH-aligned class semantics.

## classify_state(diagnostic, runtime_context) -> SystemStateClass

```text
FUNCTION classify_state(diagnostic, runtime_context):
  IF runtime_context.safe_halt_active:
    RETURN SAFE_HALT

  IF runtime_context.containment_active:
    RETURN CONTAINED

  IF diagnostic.admissibility_status == VALID AND diagnostic.normalization_status == ALREADY_VALID:
    RETURN STABLE

  IF diagnostic.admissibility_status == TRANSFORMATION_COMPATIBLE:
    IF correction_path_known(diagnostic):
      RETURN CORRECTABLE
    RETURN UNSTABLE

  IF diagnostic.admissibility_status == TRANSFORMATION_INCOMPATIBLE:
    IF fallback_candidate_exists(diagnostic):
      RETURN DEGRADED
    RETURN FAILED

  RETURN DEGRADED
END FUNCTION
```
