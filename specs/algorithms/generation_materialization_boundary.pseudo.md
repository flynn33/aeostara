
# Generation Materialization Boundary

```text
FUNCTION create_generation_plan(inputs) -> GenerationPlan
  REQUIRE no filesystem, network, or platform mutation side effects
  plan = deterministic_plan(inputs)
  RETURN plan with planHash
END FUNCTION

FUNCTION create_artifact_emission_plan(plan) -> ArtifactEmissionPlan
  REQUIRE every artifact traces to a plan element
  REQUIRE emitter invents no semantics not present in plan
  RETURN ArtifactEmissionPlan
END FUNCTION
```
