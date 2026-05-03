
# Diagnostic Chain Integrity

```text
FUNCTION validate_diagnostic_chain(chain) -> Result
  REQUIRE chain.diagnostics is non-empty
  REQUIRE first diagnostic diagnosticID == chain.rootDiagnosticID
  FOR diagnostic IN chain.diagnostics:
    REQUIRE diagnostic.chainRootReference == chain.rootDiagnosticID
    REQUIRE diagnostic.ruleReferences not empty
    IF diagnostic.diagnosticID == chain.rootDiagnosticID:
      REQUIRE diagnostic.parentDiagnosticID == null
    ELSE:
      REQUIRE diagnostic.parentDiagnosticID references an earlier diagnostic
END FUNCTION
```
