# State Normalization

Normalizes observed runtime/product state into deterministic, ASH-evaluable canonical input.

## normalize_state(observed_system_state) -> normalized_state

```text
FUNCTION normalize_state(observed_system_state):
  ASSERT observed_system_state is present

  normalized = {}
  normalized.observation_id = observed_system_state.observationID
  normalized.timestamp = observed_system_state.observedAt

  -- Deterministic field extraction
  normalized.runtime_signals = extract_runtime_signals(observed_system_state.rawState)
  normalized.config_signals = extract_config_signals(observed_system_state.rawState)
  normalized.integrity = observed_system_state.integrity

  -- Canonical ordering for deterministic downstream mapping
  normalized.runtime_signals = sort_keys_recursively(normalized.runtime_signals)
  normalized.config_signals = sort_keys_recursively(normalized.config_signals)

  RETURN normalized
END FUNCTION
```

## blocked normalization

If required source fields are missing or malformed, normalization returns blocked status with a diagnostic-ready reason. No guessing is allowed.
