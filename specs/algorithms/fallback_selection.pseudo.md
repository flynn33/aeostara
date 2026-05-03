
# Fallback Selection

Fallback is registry-driven and policy-constrained.

```text
FUNCTION select_fallback(registry, diagnostic, policy) -> FallbackDecision
  candidates = registry.candidates ordered by registry priority
  FOR candidate IN candidates:
    IF policy allows candidate and candidate validates against ASH state semantics:
      RETURN SELECTED with diagnosticReference
  RETURN UNAVAILABLE with escalation diagnostic
END FUNCTION
```
