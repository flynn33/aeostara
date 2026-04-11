# Drift Analysis (Legacy Helper)

Status: legacy helper only.

This file may be used to extract superficial observed-vs-intent differences as execution evidence. It is explicitly non-authoritative for semantic decisions.

All semantic decisions must flow through:

- `state_normalization.pseudo.md`
- `state_to_ash_mapping.pseudo.md`
- `ash_diagnostic_evaluation.pseudo.md`
- `state_classification.pseudo.md`
- `recovery_category_selection.pseudo.md`

## produce_drift_evidence(observed_state, desired_intent) -> list

```text
FUNCTION produce_drift_evidence(observed_state, desired_intent):
  RETURN shallow_or_deep_diff(observed_state, desired_intent)
END FUNCTION
```
