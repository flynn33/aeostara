
# Mapping Failure Handling

Ambiguous or blocked mapping must emit diagnostics and must not silently coerce state.

```text
FUNCTION mapping_failure_handling(status, coordinate, evidence) -> MappingResult
  diagnostic = DiagnosticEnvelope(kind=MAPPING, severity=ERROR, ruleReferences=[ASH-STATE-VALIDITY-001])
  IF status == AMBIGUOUS:
    ambiguity = MappingAmbiguity(coordinate, evidence, diagnostic)
    RETURN MappingResult(status=AMBIGUOUS, ambiguities=[ambiguity], diagnosticReferences=[diagnostic.ref])
  IF status IN [BLOCKED, FAILED]:
    RETURN MappingResult(status=status, diagnosticReferences=[diagnostic.ref])
END FUNCTION
```
