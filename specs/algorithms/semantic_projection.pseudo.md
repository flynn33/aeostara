
# Semantic Projection

Aeostara projects JSON/configuration evidence into the full 9-coordinate ASH state.

## Coordinate Bindings

| Coordinate | Required binding evidence |
|---|---|
| b0 | enabled/disabled intent signal |
| b1 | policy-permitted mutation signal |
| b2 | backup readiness signal |
| b3 | verification readiness signal |
| b4 | fallback availability signal |
| b5 | containment boundary status |
| b6 | rollback availability signal |
| b7 | audit-chain continuity signal |
| b8 | terminal/safe-halt signal |

```text
FUNCTION project_semantics(observed, desired, projection_spec) -> MappingResult
  bindings = []
  FOR coordinate IN [b0,b1,b2,b3,b4,b5,b6,b7,b8]:
    evidence = collect_pointer_evidence(coordinate, observed, desired, projection_spec)
    confidence = evaluate_mapping_confidence(coordinate, evidence)
    IF confidence.status == AMBIGUOUS:
      RETURN mapping_failure_handling(AMBIGUOUS, coordinate, evidence)
    IF confidence.status == BLOCKED:
      RETURN mapping_failure_handling(BLOCKED, coordinate, evidence)
    bindings.append(SemanticDimensionBinding(coordinate, evidence))
  state = AshState(coordinates = bindings mapped to bits b0..b8)
  RETURN MappingResult(status=MAPPED, projectedState=state, dimensionBindings=bindings)
END FUNCTION
```
