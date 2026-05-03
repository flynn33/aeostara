
# Mutation Precondition Check

No mutation may execute without a precondition check tied to diagnostics.

```text
FUNCTION check_mutation_precondition(document, operation) -> PreconditionResult
  current = resolve_pointer(document, operation.path.pointer)
  IF operation.op == "replace" OR operation.op == "remove":
    IF current.pointsToMissing:
      RETURN BLOCKED with DiagnosticEnvelope(kind=JSON_SEMANTICS)
  IF operation.preconditionHash does not match canonical_hash(current.value):
    RETURN BLOCKED with DiagnosticEnvelope(kind=JSON_SEMANTICS)
  IF operation.op == "add" AND parent pointer is missing:
    RETURN BLOCKED with DiagnosticEnvelope(kind=JSON_SEMANTICS)
  RETURN ALLOWED
END FUNCTION
```
