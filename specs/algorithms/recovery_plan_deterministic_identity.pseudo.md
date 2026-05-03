
# Recovery Plan Deterministic Identity

```text
FUNCTION recovery_plan_hash(plan_without_runtime_fields) -> SHA256_HEX
  semantic_plan = remove fields [createdAt, runtimeEventID, timestamps]
  canonical = canonicalize_json(semantic_plan)
  RETURN sha256(canonical)
END FUNCTION
```

Plan identity is separate from runtime execution event identity.
