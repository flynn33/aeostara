
# Axiom Evaluation Binding

```text
FUNCTION evaluate_axiom(axiom_id, evidence) -> AxiomDiagnostic
  result = deterministic_rule_evaluation(axiom_id, evidence)
  diagnostic = DiagnosticEnvelope(kind=STATE_VALIDITY, ruleReferences=[rule_for_axiom(axiom_id)])
  RETURN AxiomDiagnostic(axiom_id, diagnostic, result, evidence)
END FUNCTION
```
