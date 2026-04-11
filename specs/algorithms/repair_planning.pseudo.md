# Repair Planning (Legacy Helper)

Status: legacy helper only.

CRUD-style action lists are subordinate actuator helpers. Top-level planning authority is `recovery_plan_generation.pseudo.md`.

## to_actuator_mutations(evidence) -> steps

```text
FUNCTION to_actuator_mutations(evidence):
  RETURN deterministic_mutation_steps(evidence)
END FUNCTION
```
