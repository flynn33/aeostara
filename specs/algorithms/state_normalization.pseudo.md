
# State Normalization

Normalization is deterministic on the full 9-bit ASH state.

```text
FUNCTION normalize_state(candidate_state, canonical_codeword_set) -> NormalizationResult
  REQUIRE candidate_state has exactly 9 binary coordinates
  diagnostic = diagnose_state_validity(candidate_state)
  IF diagnostic.admissibilityStatus == VALID:
    RETURN {status: ALREADY_VALID, normalizedState: candidate_state, diagnostic}
  IF diagnostic.admissibilityStatus == TRANSFORMATION_COMPATIBLE:
    path = deterministic_lowest_lexicographic_codeword_path(candidate_state, canonical_codeword_set)
    IF path exists:
      RETURN {status: NORMALIZED, normalizedState: apply(path), diagnostic}
  RETURN {status: BLOCKED, diagnostic}
END FUNCTION
```
