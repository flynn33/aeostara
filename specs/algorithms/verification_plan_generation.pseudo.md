
# Verification Plan Generation

```text
FUNCTION generate_verification_plan(desired_semantic_state, recovery_goal) -> VerificationPlan
  checks = deterministic checks covering desired state, mutation effect, diagnostic emission, and audit chain
  RETURN VerificationPlan(generatedBeforeMutation=true, expectedSemanticState=desired_semantic_state, checks=checks)
END FUNCTION
```
