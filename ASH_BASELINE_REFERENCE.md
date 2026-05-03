
# ASH Baseline Reference

Aeostara conforms to the ASH Pattern System as fixed upstream authority. This repository records the baseline used for this implementation and does not modify ASH.

## Baseline

| Field | Value |
|---|---|
| Upstream repository | `/Users/jim/AI/Codex/ASH-Pattern-System` |
| Branch | `main` |
| Commit | `e123f5d7fdbb381179971f721a3292c31eb1cbc2` |
| Role | Fixed upstream semantic authority |
| Aeostara rule | If Aeostara conflicts with ASH, Aeostara changes |

## Required ASH Source Areas

| ASH area | Source path | Aeostara binding |
|---|---|---|
| State space | `specs/core/ash-state-space.pseudo.md` | `specs/ash_baseline/ash_state_space_binding.md` |
| Canonical codeword set | `specs/core/codeword-set.pseudo.md` | `specs/ash_baseline/canonical_codeword_set_binding.md` |
| Codeword transformation | `specs/algorithms/codeword-transformation-semantics.pseudo.md` | `specs/ash_baseline/codeword_transformation_binding.md` |
| State admissibility | `specs/core/state-admissibility.pseudo.md` | `specs/ash_baseline/state_admissibility_binding.md` |
| State-validity diagnostics | `specs/core/state-validity-diagnostics.pseudo.md` | `specs/ash_baseline/state_validity_diagnostic_binding.md` |
| System-state classification | `specs/core/system-state-classification.pseudo.md` | `specs/ash_baseline/system_state_classification_binding.md` |
| Recoverability | `specs/core/recoverability-semantics.pseudo.md` | `specs/ash_baseline/recoverability_binding.md` |
| Fallback policy registry | `specs/registries/fallback-policy-registry.md` | `specs/ash_baseline/fallback_policy_registry_binding.md` |
| Containment and safe halt | `specs/algorithms/containment-safe-failure-semantics.pseudo.md` | `specs/ash_baseline/containment_safe_halt_binding.md` |
| Realm identity | `specs/core/realm-identity.pseudo.md` | `specs/ash_baseline/realm_identity_binding.md` |
| Transition registry | `specs/algorithms/transition-system.pseudo.md` | `specs/ash_baseline/transition_registry_binding.md` |
| Topology generator | `specs/algorithms/topology-expansion.pseudo.md` | `specs/ash_baseline/topology_generator_binding.md` |
| Axiom evaluator | `specs/algorithms/axiom-evaluation.pseudo.md` | `specs/ash_baseline/axiom_evaluator_binding.md` |
| Generation and materialization | `specs/algorithms/generation-planning.pseudo.md` and `specs/interfaces/contracts/artifact-emitter-contract.md` | `specs/ash_baseline/generation_materialization_boundary.md` |
| Invariant categories | `specs/verification/conformance-categories.md` and `specs/verification/invariant-spec.md` | `specs/ash_baseline/invariant_coverage_map.md` |

## Non-Modification Statement

ASH was read as an upstream source and was not modified by this Aeostara implementation pass.
