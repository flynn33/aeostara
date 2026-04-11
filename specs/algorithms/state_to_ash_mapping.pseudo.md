# State To ASH Mapping

Maps normalized product/runtime state into ASH-aligned semantic input structures.

## map_to_ash_state(normalized_state, desired_system_intent) -> mapped_input

```text
FUNCTION map_to_ash_state(normalized_state, desired_system_intent):
  ASSERT normalized_state is deterministic
  ASSERT desired_system_intent is present

  mapped_input = {}
  mapped_input.observation_id = normalized_state.observation_id
  mapped_input.intent_id = desired_system_intent.intentID

  mapped_input.semantic_dimensions = derive_semantic_dimensions(
    normalized_state.runtime_signals,
    normalized_state.config_signals,
    desired_system_intent.intentState
  )

  mapped_input.dimension_confidence = evaluate_dimension_confidence(mapped_input.semantic_dimensions)

  IF has_ambiguity(mapped_input.dimension_confidence):
    mapped_input.mapping_status = "AMBIGUOUS"
    mapped_input.block_reason = "semantic dimension confidence below threshold"
  ELSE:
    mapped_input.mapping_status = "MAPPED"

  RETURN mapped_input
END FUNCTION
```

## ambiguity behavior

Ambiguous mapping is not silently coerced. Ambiguity must feed diagnostics and downstream recoverability decisions.
