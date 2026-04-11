# Fallback Selection

Selects fallback state deterministically from canonical fallback-policy registry.

## select_fallback(diagnostic, fallback_registry) -> FallbackDecision

```text
FUNCTION select_fallback(diagnostic, fallback_registry):
  decision = FallbackDecision(required=TRUE)

  IF fallback_registry is unavailable:
    decision.selectionOutcome = ESCALATE_TO_CONTAINMENT
    decision.reason = "fallback registry unavailable"
    RETURN decision

  candidates = fallback_registry.get_candidates_for(diagnostic)
  candidates = sort_by_rank_then_policy_id(candidates)

  IF candidates is empty:
    decision.selectionOutcome = ESCALATE_TO_CONTAINMENT
    decision.reason = "no fallback candidate"
    RETURN decision

  candidate = first_validated_candidate(candidates)
  IF candidate is NONE:
    decision.selectionOutcome = ESCALATE_TO_CONTAINMENT
    decision.reason = "all candidates invalid"
    RETURN decision

  decision.policyID = candidate.policy_id
  decision.candidateStateReference = candidate.state_reference
  decision.selectionOutcome = SELECTED
  decision.reason = "fallback candidate selected and validated"
  RETURN decision
END FUNCTION
```
