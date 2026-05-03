
# Transition Registry Binding

```text
FUNCTION resolve_transition(state, transition_id, registry) -> TransitionResult
  transition = registry.lookup(transition_id)
  IF transition is missing:
    RETURN blocked diagnostic
  RETURN apply_codeword_transformation(state, transition.codeword)
END FUNCTION
```
